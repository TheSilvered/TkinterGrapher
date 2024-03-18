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
        self.graph_canvas = GraphCanvas(canvas)
        self.graphers = [
            (LineType1(self.graph_canvas, self.root), "#DD0000"),
            (Sine(self.graph_canvas, self.root), "#00DD00"),
            (Parabola(self.graph_canvas, self.root), "#0000DD"),
        ]
        ttk.Button(frame, text="Refresh", command=self.redraw_canvas).grid(row=row, column=0, sticky=tk.NE)
        row += 1

        for i, (grapher, _) in enumerate(self.graphers):
            grapher.params.build_widget(frame).grid(column=0, row=row + i)
        row += len(self.graphers) + 1

        canvas.grid(column=0, row=row)
        canvas.rowconfigure(0, weight=1)
        canvas.columnconfigure(0, weight=1)
        row += 1

        canvas.bind("<Button-1>", self.handle_button_press)
        canvas.bind("<B1-Motion>", self.handle_motion)

    def handle_button_press(self, event):
        self.initial_cart = (
            self.graph_canvas.x_canvas_to_x_plane(event.x),
            self.graph_canvas.y_canvas_to_y_plane(event.y)
        )
        self.initial_x_range = self.graph_canvas.x_range()
        self.initial_y_range = self.graph_canvas.y_range()

    def handle_motion(self, event):
        if None in (self.initial_cart, self.initial_x_range, self.initial_y_range):
            return
        self.graph_canvas.set_x_range(self.initial_x_range)
        self.graph_canvas.set_y_range(self.initial_y_range)

        x_cart = self.graph_canvas.x_canvas_to_x_plane(event.x)
        y_cart = self.graph_canvas.y_canvas_to_y_plane(event.y)

        diff_x = self.initial_cart[0] - x_cart
        diff_y = y_cart - self.initial_cart[1]

        self.graph_canvas.set_x_range((self.initial_x_range[0] + diff_x, self.initial_x_range[1] + diff_x))
        self.graph_canvas.set_y_range((self.initial_y_range[0] + diff_y, self.initial_y_range[1] + diff_y))

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
