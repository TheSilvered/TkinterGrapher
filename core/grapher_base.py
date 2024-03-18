from abc import ABC, abstractmethod
from typing import Callable

from .graph_canvas import GraphCanvasBase
from .param_input import ParamInputBase, ParamInput
from tkinter import Tk


class GrapherBase(ABC):
    def __init__(self, graph_canvas: GraphCanvasBase, window: Tk | None, input_cls: type = ParamInput) -> None:
        self.graph_canvas = graph_canvas
        self.window = window
        self.params: ParamInputBase = input_cls(self.get_param_string(), window)

    @abstractmethod
    def get_param_string(self) -> str:
        pass

    @abstractmethod
    def graph(self):
        pass


class FunctionGraph(GrapherBase, ABC):
    def __init__(self, graph_canvas: GraphCanvasBase, window: Tk | None, input_cls: type = ParamInput):
        super().__init__(graph_canvas, window, input_cls)
        self.__func = self.get_func()

    def graph(self):
        if not self.params.available():
            return

        points = []

        arg_names = self.params.get_names()
        values = (self.params[name] for name in arg_names)
        kwargs = dict(zip(arg_names, values))

        for x_canvas in range(*self.graph_canvas.canvas_x_range):
            x = self.graph_canvas.x_canvas_to_x_plane(x_canvas)
            y = self.__func(x, **kwargs)
            y_canvas = self.graph_canvas.y_plane_to_y_canvas(y)
            points.append((x_canvas, y_canvas))
        self.graph_canvas.lines(points)

    @abstractmethod
    def get_func(self) -> Callable:
        pass
