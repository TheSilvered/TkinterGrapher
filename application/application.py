import platform

import tkinter as tk
from tkinter import ttk
from core.graph_canvas import GraphCanvas
from function_impls.line_type_1 import LineType1
from function_impls.sine import Sine
from function_impls.parabola import Parabola


class Application:
    def __init__(self):
        self.initial_y_range: tuple | None = None
        self.initial_cart: tuple | None = None
        self.initial_x_range: tuple | None = None
        self.graph_canvas = None
        self.graphers = []

        self.root = tk.Tk()
        self.root.title("Tkinter Grapher")
        self.__build_gui()
        self.redraw_canvas()

    def __build_gui(self):
        self.root.grid()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.resizable(False, False)

        frame = ttk.Frame(self.root)
        frame.grid()
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        canvas = tk.Canvas(frame, width=500, height=500)

        row = 0
        self.graph_canvas = GraphCanvas(canvas, x_range=(-5, 5), y_range=(-5, 5))
        self.graphers = [
            (LineType1(self.graph_canvas, self.root), "#DD0000"),
            (Sine(self.graph_canvas, self.root), "#00DD00"),
            (Parabola(self.graph_canvas, self.root), "#0000DD"),
        ]

        for i, (grapher, _) in enumerate(self.graphers):
            param_widget = grapher.params.build_widget(frame)
            param_widget.grid(column=0, row=row + i)
            for child in param_widget.winfo_children():
                if isinstance(child, ttk.Entry) or isinstance(child, tk.Entry):
                    child.bind("<Return>", self.handle_return_event)
                    child.bind("<Button-1>", self.handle_return_event)
                    child.bind("<KeyPress>", self.handle_return_event)
                    child.bind("<KeyRelease>", self.handle_return_event)
        row += len(self.graphers) + 1

        canvas.grid(column=0, row=row)
        canvas.rowconfigure(0, weight=1)
        canvas.columnconfigure(0, weight=1)
        row += 1

        canvas.bind("<Button-1>", self.handle_button_press)
        canvas.bind("<B1-Motion>", self.handle_motion)
        canvas.bind("<MouseWheel>", self.handle_scroll)
        canvas.bind("<Button-4>", self.handle_scroll)
        canvas.bind("<Button-5>", self.handle_scroll)

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
        if event.type == 4:  # button press, running on Linux
            if event.num == 4:
                step = 1
            else:
                step = 2
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
        for grapher, color in self.graphers:
            self.graph_canvas.style["fill"] = color
            grapher.graph()
        self.graph_canvas.draw_foreground()

    def run(self):
        self.root.mainloop()
