from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import font as tk_font
from itertools import chain
from math import floor, ceil


class GraphCanvasBase(ABC):
    def __init__(self, x_range=(-10, 10), y_range=(-10, 10)):
        self._x_range = x_range
        self._y_range = y_range

    @abstractmethod
    def width(self) -> int:
        pass

    @abstractmethod
    def height(self) -> int:
        pass

    @property
    def x_range(self) -> tuple[float, float]:
        return self._x_range

    @property
    def y_range(self) -> tuple[float, float]:
        return self._y_range

    @x_range.setter
    def x_range(self, range_: tuple[float, float] | list[float]):
        self._x_range = tuple(range_)

    @y_range.setter
    def y_range(self, range_: tuple[float, float] | list[float]):
        self._y_range = tuple(range_)

    @property
    @abstractmethod
    def canvas_x_range(self) -> tuple[int, int]:
        pass

    @property
    @abstractmethod
    def canvas_y_range(self) -> tuple[int, int]:
        pass

    @abstractmethod
    def line(self, p1: tuple[int, int], p2: tuple[int, int]):
        pass

    @abstractmethod
    def lines(self, points: list[tuple[int, int]]):
        pass

    @abstractmethod
    def circle(self, center: tuple[int, int], radius: int):
        pass

    @abstractmethod
    def ellipse(self, p1: tuple[int, int], p2: tuple[int, int]):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def draw_background(self):
        pass

    @abstractmethod
    def draw_foreground(self):
        pass

    def x_plane_to_x_canvas(self, x):
        min_x, max_x = self.x_range
        min_xc, max_xc = self.canvas_x_range
        if max_x == min_x:
            return max_x
        return (x - min_x) / (max_x - min_x) * (max_xc - min_xc) + min_xc

    def y_plane_to_y_canvas(self, y):
        min_y, max_y = self.y_range
        min_yc, max_yc = self.canvas_y_range
        if max_y == min_y:
            return max_y
        return (y - min_y) / (max_y - min_y) * (max_yc - min_yc) + min_yc

    def x_canvas_to_x_plane(self, xc):
        min_x, max_x = self.x_range
        min_xc, max_xc = self.canvas_x_range
        if max_xc == min_xc:
            return max_xc
        return (xc - min_xc) / (max_xc - min_xc) * (max_x - min_x) + min_x

    def y_canvas_to_y_plane(self, yc):
        min_y, max_y = self.y_range
        min_yc, max_yc = self.canvas_y_range
        if max_yc == min_yc:
            return max_yc
        return (yc - min_yc) / (max_yc - min_yc) * (max_y - min_y) + min_y


class GraphCanvas(GraphCanvasBase):
    def __init__(self, canvas: tk.Canvas, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.canvas = canvas
        self.style = {
            "fill": "#DD0000",
            "width": 2
        }

    def width(self) -> int:
        return int(self.canvas.cget("width"))

    def height(self) -> int:
        return int(self.canvas.cget("height"))

    @property
    def canvas_x_range(self) -> tuple[float, float]:
        return 0, self.width()

    @property
    def canvas_y_range(self) -> tuple[float, float]:
        return self.height(), 0

    def line(self, p1: tuple[int, int], p2: tuple[int, int]):
        self.canvas.create_line(*p1, *p2, **self.style)

    def lines(self, points: list[tuple[int, int]]):
        self.canvas.create_line(*chain(points), **self.style)

    def ellipse(self, p1: tuple[int, int], p2: tuple[int, int]):
        self.canvas.create_oval(*p1, *p2, **self.style)

    def circle(self, center: tuple[int, int], radius: int):
        x1 = center[0] - radius
        y1 = center[1] - radius
        x2 = center[0] + radius + 1
        y2 = center[1] + radius + 1
        self.canvas.create_oval(x1, y1, x2, y2, **self.style)

    def clear(self):
        self.canvas.delete("all")

    def draw_background(self):
        w = self.width()
        h = self.height()

        self.canvas.create_rectangle(0, 0, w, h, width=0, fill="#FFFFFF")

        min_x, max_x = self.x_range
        for x in range(int(ceil(min_x)), int(ceil(max_x))):
            x_canvas = self.x_plane_to_x_canvas(x)
            self.canvas.create_line(x_canvas, 0, x_canvas, h, fill="#DDDDDD")

        min_y, max_y = self.y_range
        for y in range(int(ceil(min_y)), int(ceil(max_y))):
            y_canvas = self.y_plane_to_y_canvas(y)
            self.canvas.create_line(0, y_canvas, w, y_canvas, fill="#DDDDDD")

        y_x_line = self.y_plane_to_y_canvas(0)
        x_y_line = self.x_plane_to_x_canvas(0)
        self.canvas.create_line(0, y_x_line, w, y_x_line, fill="#000000", arrow=tk.LAST)
        self.canvas.create_line(x_y_line, 0, x_y_line, h, fill="#000000", arrow=tk.FIRST)

    def __draw_x_coordinate(self, x, y, font, text):
        line_height = font.metrics("linespace")
        y += 5
        color = "#000000"
        if y < 5:
            y = 5
            color = "#888888"
        elif y > self.height() - line_height - 5:
            y = self.height() - line_height - 5
            color = "#888888"
        self.canvas.create_text(x, y, text=text, fill=color, anchor="n")

    def __draw_y_coordinate(self, x, y, font, text):
        line_width = font.measure(text)
        x -= 5
        color = "#000000"
        if x > self.width() - 5:
            x = self.width() - 5
            color = "#888888"
        elif x < line_width + 5:
            x = line_width + 5
            color = "#888888"
        self.canvas.create_text(x, y, text=text, fill=color, anchor="e")

    def draw_foreground(self):
        font = tk_font.Font(font="TkDefaultFont")

        y_center = self.y_plane_to_y_canvas(0)
        min_x, max_x = self.x_range
        for x in range(int(floor(min_x)), int(ceil(max_x)) + 1):
            if x == 0:
                continue
            x_canvas = self.x_plane_to_x_canvas(x)
            self.__draw_x_coordinate(x_canvas, y_center, font, str(x))

        x_center = self.x_plane_to_x_canvas(0)
        min_y, max_y = self.y_range
        for y in range(int(floor(min_y)), int(ceil(max_y)) + 1):
            if y == 0:
                continue
            y_canvas = self.y_plane_to_y_canvas(y)
            self.__draw_y_coordinate(x_center, y_canvas, font, str(y))

        self.canvas.create_text(x_center - 5, y_center + 5, text="0", fill="#000000", anchor="ne")
