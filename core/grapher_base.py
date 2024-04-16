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

    @staticmethod
    @abstractmethod
    def get_param_string() -> str:
        pass

    @abstractmethod
    def graph(self):
        pass


class FunctionGraphX(GrapherBase, ABC):
    def __init__(self, graph_canvas: GraphCanvasBase, window: Tk | None, input_cls: type = ParamInput):
        super().__init__(graph_canvas, window, input_cls)
        self.__func = self.get_func()

    def __clamp_line(self, p1, p2):
        """p1 is inside the plane, p2 is not, finds the intersection with the edge of the canvas.
        p1 is a point of the canvas, p2 is a point of the plane"""
        p1x = self.graph_canvas.x_canvas_to_x_plane(p1[0])
        p1y = self.graph_canvas.y_canvas_to_y_plane(p1[1])

        min_y, max_y = self.graph_canvas.y_range
        min_yc, max_yc = self.graph_canvas.canvas_y_range
        if p2[1] < min_y:
            py = min_y
            py_canvas = min_yc
        else:
            py = max_y
            py_canvas = max_yc
        if p1y == p2[1]:
            return p1
        inv_m = (p1x - p2[0]) / (p1y - p2[1])
        px = (py - p1y) * inv_m + p1x
        px_canvas = self.graph_canvas.x_plane_to_x_canvas(px)
        return px_canvas, py_canvas

    def graph(self):
        if not self.params.available():
            return

        final_points = []
        points = []

        prev_invalid_point = None

        arg_names = self.params.get_names()
        values = (self.params[name] for name in arg_names)
        kwargs = dict(zip(arg_names, values))
        min_y, max_y = self.graph_canvas.y_range
        min_xc, max_xc = self.graph_canvas.canvas_x_range

        for x_canvas in range(min_xc, max_xc, 1 if min_xc <= max_xc else -1):
            x = self.graph_canvas.x_canvas_to_x_plane(x_canvas)
            try:
                y = self.__func(x, **kwargs)
            except Exception:
                if points:
                    final_points.append(points)
                points = []
                continue
            if not isinstance(y, float) and not isinstance(y, int):
                if points:
                    final_points.append(points)
                points = []
                continue
            y_canvas = self.graph_canvas.y_plane_to_y_canvas(y)
            if y < min_y or y > max_y:
                prev_invalid_point = (x, y)
                if points:
                    points.append(self.__clamp_line(points[-1], prev_invalid_point))
                    final_points.append(points)
                points = []
                continue
            elif prev_invalid_point is not None:
                points.append(self.__clamp_line((x_canvas, y_canvas), prev_invalid_point))
                prev_invalid_point = None
            points.append((x_canvas, y_canvas))

        if points:
            final_points.append(points)
        for p_list in final_points:
            self.graph_canvas.lines(p_list)

    @abstractmethod
    def get_func(self) -> Callable:
        pass


class FunctionGraphY(GrapherBase, ABC):
    def __init__(self, graph_canvas: GraphCanvasBase, window: Tk | None, input_cls: type = ParamInput):
        super().__init__(graph_canvas, window, input_cls)
        self.__func = self.get_func()

    def __clamp_line(self, p1, p2):
        """p1 is inside the plane, p2 is not, finds the intersection with the edge of the canvas.
        p1 is a point of the canvas, p2 is a point of the plane"""
        p1x = self.graph_canvas.x_canvas_to_x_plane(p1[0])
        p1y = self.graph_canvas.y_canvas_to_y_plane(p1[1])

        min_x, max_x = self.graph_canvas.x_range
        min_xc, max_xc = self.graph_canvas.canvas_x_range
        if p2[0] < min_x:
            px = min_x
            px_canvas = min_xc
        else:
            px = max_x
            px_canvas = max_xc
        if p1x == p2[0]:
            return px
        m = (p1y - p2[1]) / (p1x - p2[0])
        py = (px - p1x) * m + p1y
        py_canvas = self.graph_canvas.y_plane_to_y_canvas(py)
        return px_canvas, py_canvas

    def graph(self):
        if not self.params.available():
            return

        final_points = []
        points = []

        prev_invalid_point = None

        arg_names = self.params.get_names()
        values = (self.params[name] for name in arg_names)
        kwargs = dict(zip(arg_names, values))
        min_x, max_x = self.graph_canvas.x_range
        min_yc, max_yc = self.graph_canvas.canvas_y_range

        for y_canvas in range(min_yc, max_yc, 1 if min_yc <= max_yc else -1):
            y = self.graph_canvas.y_canvas_to_y_plane(y_canvas)
            try:
                x = self.__func(y, **kwargs)
            except Exception:
                if points:
                    final_points.append(points)
                points = []
                continue
            if not isinstance(x, float) and not isinstance(x, int):
                if points:
                    final_points.append(points)
                points = []
                continue
            x_canvas = self.graph_canvas.x_plane_to_x_canvas(x)
            if x < min_x or x > max_x:
                prev_invalid_point = (x, y)
                if points:
                    points.append(self.__clamp_line(points[-1], prev_invalid_point))
                    final_points.append(points)
                points = []
                continue
            elif prev_invalid_point is not None:
                points.append(self.__clamp_line((x_canvas, y_canvas), prev_invalid_point))
                prev_invalid_point = None
            points.append((x_canvas, y_canvas))

        if points:
            final_points.append(points)
        for p_list in final_points:
            self.graph_canvas.lines(p_list)

    @abstractmethod
    def get_func(self) -> Callable:
        pass
