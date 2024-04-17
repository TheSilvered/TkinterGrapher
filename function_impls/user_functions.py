from typing import Callable
import tkinter as tk
from core import GraphCanvas, FunctionGraphX, FunctionGraphY, FunctionInput


class FunctionX(FunctionGraphX):
    def __init__(self, graph_canvas: GraphCanvas, window: tk.Tk | None):
        super().__init__(graph_canvas, window, FunctionInput)

    @staticmethod
    def get_param_string() -> str:
        return "f(x)"

    def get_func(self) -> Callable:
        return self.f

    def f(self, x):
        return self.params[x]


class FunctionY(FunctionGraphY):
    def __init__(self, graph_canvas: GraphCanvas, window: tk.Tk | None):
        super().__init__(graph_canvas, window, FunctionInput)

    @staticmethod
    def get_param_string() -> str:
        return "f(y)"

    def get_func(self) -> Callable:
        return self.f

    def f(self, y):
        return self.params[y]
