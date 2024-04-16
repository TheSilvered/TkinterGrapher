import platform

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from core.graph_canvas import GraphCanvas
from function_impls.lines import LineType1, LineType2
from function_impls.sine import Sine
from function_impls.parabola import Parabola
from function_impls.logarithm import Logarithm
from function_impls.roots import NthRoot, SquareRoot
from function_impls.user_functions import FunctionX, FunctionY


class Application:
    def __init__(self):
        self.initial_y_range: tuple | None = None
        self.initial_cart: tuple | None = None
        self.initial_x_range: tuple | None = None
        self.graph_canvas = None
        self.grapher_types = {}
        self.graphers = []
        self.grapher_frame: tk.Widget | None = None

        self.colors = [
            "#F9102F",
            "#3FD258",
            "#3572EC",
            "#FF7800",
            "#00C9FF",
            "#AD00FF",
            "#000000"
        ]
        self.color_index = 0

        self.root = tk.Tk()
        self.root.title("Tkinter Grapher")
        self.__register_graphers()
        self.__build_gui()
        self.redraw_canvas()

    def __register_graphers(self):
        self.__register_grapher(FunctionX)
        self.__register_grapher(FunctionY)
        self.__register_grapher(LineType1)
        self.__register_grapher(LineType2)
        self.__register_grapher(Sine)
        self.__register_grapher(Parabola)
        self.__register_grapher(Logarithm)
        self.__register_grapher(SquareRoot)
        self.__register_grapher(NthRoot)

    def __register_grapher(self, grapher_class):
        self.grapher_types[grapher_class.get_param_string().replace("$", "")] = grapher_class

    def __build_gui(self):
        self.root.grid()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root)
        frame.grid()
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        select_func = ttk.Button(frame, text="+",  width=3, command=self.function_selection_popup)
        select_func.grid(column=0, row=0, sticky=tk.W)

        self.grapher_frame = ttk.Frame(frame)
        self.grapher_frame.grid(column=0, row=1, sticky=tk.EW)

        canvas = tk.Canvas(frame, width=500, height=500)
        canvas.grid(column=0, row=2)
        canvas.rowconfigure(0, weight=1)
        canvas.columnconfigure(0, weight=1)
        canvas.bind("<Button-1>", self.handle_button_press)
        canvas.bind("<B1-Motion>", self.handle_motion)
        canvas.bind("<MouseWheel>", self.handle_scroll)
        canvas.bind("<Button-4>", self.handle_scroll)
        canvas.bind("<Button-5>", self.handle_scroll)
        self.graph_canvas = GraphCanvas(canvas, x_range=(-5, 5), y_range=(-5, 5))

    def handle_button_press(self, event):
        self.initial_cart = (
            self.graph_canvas.x_canvas_to_x_plane(event.x),
            self.graph_canvas.y_canvas_to_y_plane(event.y)
        )
        self.initial_x_range = self.graph_canvas.x_range
        self.initial_y_range = self.graph_canvas.y_range

    def handle_motion(self, event):
        if None in (self.initial_cart, self.initial_x_range, self.initial_y_range):
            return
        self.graph_canvas.x_range = self.initial_x_range
        self.graph_canvas.y_range = self.initial_y_range

        x_cart = self.graph_canvas.x_canvas_to_x_plane(event.x)
        y_cart = self.graph_canvas.y_canvas_to_y_plane(event.y)

        diff_x = self.initial_cart[0] - x_cart
        diff_y = self.initial_cart[1] - y_cart

        self.graph_canvas.x_range = self.initial_x_range[0] + diff_x, self.initial_x_range[1] + diff_x
        self.graph_canvas.y_range = self.initial_y_range[0] + diff_y, self.initial_y_range[1] + diff_y

        self.redraw_canvas()

    def handle_scroll(self, event):
        if event.type == "4":  # button press, running on Linux
            if event.num == 4:
                step = 1
            else:
                step = -1
        elif platform.system() == "Windows":
            step = event.delta // 120
        else:
            step = event.delta

        min_x, max_x = self.graph_canvas.x_range
        min_y, max_y = self.graph_canvas.y_range
        x = self.graph_canvas.x_canvas_to_x_plane(event.x)
        y = self.graph_canvas.y_canvas_to_y_plane(event.y)
        x_range = max_x - min_x
        y_range = max_y - min_y

        if step < 0:
            new_x_range = x_range * (10 / 9)
            new_y_range = y_range * (10 / 9)
        elif step > 0:
            new_x_range = x_range * (9 / 10)
            new_y_range = y_range * (9 / 10)
        else:
            return

        x_diff = x_range - new_x_range
        y_diff = y_range - new_y_range
        if x_range == 0:
            x_weight = .5
        else:
            x_weight = (x - min_x) / x_range

        if y_range == 0:
            y_weight = .5
        else:
            y_weight = (y - min_y) / y_range

        self.graph_canvas.x_range = min_x + x_diff * x_weight, max_x - x_diff * (1 - x_weight)
        self.graph_canvas.y_range = min_y + y_diff * y_weight, max_y - y_diff * (1 - y_weight)

        self.redraw_canvas()

    def handle_return_event(self, _):
        self.redraw_canvas()

    def redraw_canvas(self):
        self.graph_canvas.clear()
        self.graph_canvas.draw_background()
        for grapher, color, visible in self.graphers:
            if not visible.get():
                continue
            self.graph_canvas.style["fill"] = color
            grapher.graph()
        self.graph_canvas.draw_foreground()

    def function_selection_popup(self):
        popup = tk.Toplevel()
        popup.title("New graph")
        popup.grab_set()
        popup.geometry("250x75")
        popup.resizable(False, False)
        label = ttk.Label(popup, text="Select a graph to add:")
        label.pack()
        combobox = ttk.Combobox(popup, values=list(self.grapher_types.keys()))
        combobox.pack()
        close = ttk.Button(popup, text="Ok", command=lambda: self.add_function(combobox.get(), popup))
        close.pack()

    def add_function(self, type_, popup):
        popup.destroy()
        if type_ not in self.grapher_types:
            return
        grapher_type = self.grapher_types[type_]
        grapher = grapher_type(self.graph_canvas, self.root)
        color = self.colors[self.color_index]
        self.color_index += 1
        self.color_index %= len(self.colors)

        param_frame = ttk.Frame(self.grapher_frame)
        param_frame.pack(fill=tk.X)
        param_frame.columnconfigure(0, weight=10)
        param_frame.columnconfigure(1, weight=2)
        param_widget = grapher.params.build_widget(param_frame)
        param_widget.grid(row=0, column=0, sticky=tk.W)

        grapher_edit_frame = ttk.Frame(param_frame)
        grapher_edit_frame.grid(row=0, column=1, sticky=tk.E)

        change_color_button = None
        change_color_button = tk.Button(
            grapher_edit_frame,
            text="     ",
            bg=color,
            command=lambda: self.change_color(grapher, change_color_button),
            relief=tk.GROOVE
        )
        change_color_button.grid(row=0, column=1, sticky=tk.E)

        checkbox_var = tk.IntVar()
        visible_button = ttk.Checkbutton(
            grapher_edit_frame,
            variable=checkbox_var,
            command=self.redraw_canvas
        )
        visible_button.grid(row=0, column=2, sticky=tk.E, padx=2)
        visible_button.invoke()

        remove_button = ttk.Button(
            grapher_edit_frame,
            text="Remove",
            command=lambda: self.remove_grapher(grapher, param_frame)
        )
        remove_button.grid(row=0, column=3, sticky=tk.E)

        self.graphers.append([grapher, color, checkbox_var])

        for child in param_widget.winfo_children():
            if isinstance(child, ttk.Entry) or isinstance(child, tk.Entry):
                child.bind("<Return>", self.handle_return_event)
                child.bind("<Button-1>", self.handle_return_event)
                child.bind("<KeyPress>", self.handle_return_event)
                child.bind("<KeyRelease>", self.handle_return_event)

    def remove_grapher(self, grapher, param_frame):
        result = messagebox.askokcancel("Delete graph", "Are you sure you want to delete this graph?")
        if not result:
            return
        del self.graphers[list(map(lambda x: x[0], self.graphers)).index(grapher)]
        param_frame.pack_forget()
        param_frame.destroy()
        self.redraw_canvas()

    def change_color(self, grapher, button):
        idx = list(map(lambda x: x[0], self.graphers)).index(grapher)
        color = self.graphers[idx][1]
        new_color = colorchooser.askcolor(color)
        if new_color == (None, None):
            return
        button.configure(bg=new_color[1])
        self.graphers[idx][1] = new_color[1]
        self.redraw_canvas()

    def run(self):
        self.root.mainloop()
