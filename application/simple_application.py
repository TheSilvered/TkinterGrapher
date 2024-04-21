import tkinter as tk
from tkinter import ttk

from core import GraphCanvas, GrapherBase, FunctionInput
from function_impls.user_functions import FunctionX
from function_impls.ellipse import Circle


class SimpleApplication:
    def __init__(self):
        self.graph_canvas: GraphCanvas | None = None

        self.grapher_combobox: ttk.Combobox | None = None

        self.min_x_entry: ttk.Entry | None = None
        self.max_x_entry: ttk.Entry | None = None
        self.min_y_entry: ttk.Entry | None = None
        self.max_y_entry: ttk.Entry | None = None

        self.grapher: GrapherBase | None = None
        self.grapher_param_widget: tk.Widget | None = None
        self.grapher_frame: ttk.Frame | None = None

        self.x_entry: ttk.Entry | None = None
        self.x_label: ttk.Label | None = None

        self.available_graphers = {
            "f(x)": FunctionX,
            "Cerchio": Circle
        }

        self.default_graph = "f(x)"
        self.error_text = "Errore"

        self.root = tk.Tk()
        self.root.title("Calcolatrice Grafica")
        self.__build_ui()

    def __build_ui(self):
        self.root.resizable(False, False)

        ######################## Main application frame ########################

        frame = ttk.Frame(self.root)
        frame.grid()
        frame.columnconfigure(0, weight=1)

        ####################### Top part (controls frame) ######################

        control_frame = ttk.Frame(frame)
        control_frame.grid(row=0, column=0, sticky=tk.EW, padx=10)
        control_frame.columnconfigure(0, weight=1)

        ######################### Bottom part (canvas) #########################

        canvas = tk.Canvas(frame, width=500, height=500)
        canvas.grid(row=1, column=0)
        self.graph_canvas = GraphCanvas(canvas)
        self.graph_canvas.color = "#DD0000"
        self.graph_canvas.line_width = 2

        ########################### Controls: top row ##########################

        top_row = ttk.Frame(control_frame)
        top_row.grid(row=0, column=0, sticky=tk.EW)
        top_row.columnconfigure(0, weight=0)
        top_row.columnconfigure(1, weight=0)
        top_row.columnconfigure(2, weight=10)

        self.grapher_combobox = ttk.Combobox(top_row, values=list(self.available_graphers.keys()))
        self.grapher_combobox.grid(row=0, column=0, pady=5)
        self.grapher_combobox.insert(0, self.default_graph)

        select_button = ttk.Button(top_row, text="Seleziona", command=self.update_grapher)
        select_button.grid(row=0, column=1, padx=10)
        refresh_button = ttk.Button(top_row, text="Aggiorna", command=self.refresh)
        refresh_button.grid(row=0, column=2, sticky=tk.E)

        ######################### Controls: middle row #########################

        self.grapher_frame = ttk.Frame(control_frame)
        self.grapher_frame.grid(row=1, column=0, sticky=tk.EW)
        self.grapher_frame.columnconfigure(0, weight=1)

        self.update_grapher()

        ######################### Controls: bottom row #########################

        bottom_row = ttk.Frame(control_frame)
        bottom_row.grid(row=2, column=0, pady=5)
        bottom_row.columnconfigure(0, weight=1)

        x_range_label = ttk.Label(bottom_row, text="Range x: [")
        x_range_label.pack(side=tk.LEFT)

        self.min_x_entry = ttk.Entry(bottom_row, width=4, justify=tk.RIGHT)
        self.min_x_entry.pack(side=tk.LEFT)
        self.min_x_entry.insert(0, "-5")

        x_range_comma = ttk.Label(bottom_row, text=";")
        x_range_comma.pack(side=tk.LEFT)

        self.max_x_entry = ttk.Entry(bottom_row, width=4, justify=tk.RIGHT)
        self.max_x_entry.pack(side=tk.LEFT)
        self.max_x_entry.insert(0, "5")

        y_range_label = ttk.Label(bottom_row, text="]           Range y: [")
        y_range_label.pack(side=tk.LEFT)

        self.min_y_entry = ttk.Entry(bottom_row, width=4, justify=tk.RIGHT)
        self.min_y_entry.pack(side=tk.LEFT)
        self.min_y_entry.insert(0, "-5")

        y_range_comma = ttk.Label(bottom_row, text=";")
        y_range_comma.pack(side=tk.LEFT)

        self.max_y_entry = ttk.Entry(bottom_row, width=4, justify=tk.RIGHT)
        self.max_y_entry.pack(side=tk.LEFT)
        self.max_y_entry.insert(0, "5")

        y_range_end = ttk.Label(bottom_row, text="]")
        y_range_end.pack(side=tk.LEFT)

        self.refresh()

    def refresh(self):
        try:
            min_x = float(self.min_x_entry.get())
            max_x = float(self.max_x_entry.get())
            min_y = float(self.min_y_entry.get())
            max_y = float(self.max_y_entry.get())
        except ValueError:
            return

        if min_x >= max_x or min_y >= max_y:
            return

        self.graph_canvas.x_range = (min_x, max_x)
        self.graph_canvas.y_range = (min_y, max_y)

        if self.x_entry is not None:
            try:
                x_value = float(self.x_entry.get())
                func_value = self.grapher.params[x_value]
                if func_value is None:
                    self.x_label.configure(text=self.error_text)
                else:
                    self.x_label.configure(text=f"{func_value:.4g}")
            except ValueError:
                self.x_label.configure(text=self.error_text)

        self.graph_canvas.clear()
        self.graph_canvas.draw_background()
        self.grapher.graph()
        self.graph_canvas.draw_foreground()

    def update_grapher(self):
        name = self.grapher_combobox.get()
        if name not in self.available_graphers:
            return
        self.change_grapher(self.available_graphers[name])

    def change_grapher(self, grapher_type: type):
        if self.grapher_param_widget is not None:
            self.grapher_param_widget.grid_forget()
            self.grapher_param_widget.destroy()

        self.x_entry = None
        self.x_label = None

        self.grapher = grapher_type(self.graph_canvas)
        if isinstance(self.grapher.params, FunctionInput):
            self.grapher_param_widget = ttk.Frame(self.grapher_frame)
            param_w = self.grapher.params.build_widget(self.grapher_param_widget)
            param_w.grid(row=0, column=0)
            f_label = ttk.Label(self.grapher_param_widget, text="   f(")
            f_label.grid(row=0, column=1)
            self.x_entry = ttk.Entry(self.grapher_param_widget, width=5, justify=tk.RIGHT)
            self.x_entry.grid(row=0, column=2)
            eq_label = ttk.Label(self.grapher_param_widget, text=") =")
            eq_label.grid(row=0, column=3)
            self.x_label = ttk.Label(self.grapher_param_widget, text=self.error_text)
            self.x_label.grid(row=0, column=4)
        else:
            self.grapher_param_widget = self.grapher.params.build_widget(self.grapher_frame)
        self.grapher_param_widget.grid(row=0, column=0, sticky=tk.W)

    def run(self):
        self.root.mainloop()
