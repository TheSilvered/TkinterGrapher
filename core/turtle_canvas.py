from .graph_canvas import GraphCanvasBase
import turtle as t
import math


class TurtleCanvas(GraphCanvasBase):
    def width(self) -> int:
        return t.screensize()[0]

    def height(self) -> int:
        return t.screensize()[1]

    @property
    def canvas_x_range(self) -> tuple[int, int]:
        x = self.width() // 2
        return -x, x

    @property
    def canvas_y_range(self) -> tuple[int, int]:
        y = self.height() // 2
        return -y, y

    def __set_style(self):
        t.color(self.color)
        t.width(self.line_width)

    def line(self, p1, p2):
        self.__set_style()
        t.penup()
        t.goto(p1[0], p1[1])
        t.pendown()
        t.goto(p2[0], p2[1])
        t.penup()

    def lines(self, points):
        self.__set_style()
        t.penup()
        t.goto(*points[0])
        t.pendown()
        for p in points[1:]:
            t.goto(*p)
        t.penup()

    def circle(self, center: tuple[int, int], radius: int):
        self.__set_style()
        t.penup()
        t.seth(0)
        t.goto(center[0], center[1] - radius)
        t.pendown()
        t.circle(radius)
        t.penup()

    def ellipse(self, p1: tuple[int, int], p2: tuple[int, int]):
        self.__set_style()
        t.penup()
        a = (p2[0] - p1[0]) / 2
        b = (p2[1] - p1[1]) / 2

        # ensure that there is at least one step per pixel
        r_max = int(max(a, b) * 4)
        if r_max == 0:
            return

        for i in range(r_max + 1):
            k = i / r_max * math.pi * 2
            x = a * math.sin(k) + a
            y = b * math.cos(k) + b
            t.goto(x + p1[0], y + p1[1])
            t.pendown()
        t.penup()

    def clear(self):
        t.clearscreen()

    def draw_background(self):
        min_xc, max_xc = self.canvas_x_range
        min_yc, max_yc = self.canvas_y_range

        prev_color = self.color
        self.color = "#DDDDDD"
        min_x, max_x = self.x_range
        for x in range(int(math.floor(min_x)), int(math.ceil(max_x))):
            x_canvas = self.x_plane_to_x_canvas(x)
            self.line((x_canvas, min_yc), (x_canvas, max_yc))

        min_y, max_y = self.y_range
        for y in range(int(math.floor(min_y)), int(math.ceil(max_y))):
            y_canvas = self.y_plane_to_y_canvas(y)
            self.line((min_xc, y_canvas), (max_xc, y_canvas))

        self.color = "#000000"

        self.lines([
            (min_xc, min_yc),
            (max_xc, min_yc),
            (max_xc, max_yc),
            (min_xc, max_yc),
            (min_xc, min_yc)
        ])

        y_x_line = self.y_plane_to_y_canvas(0)
        x_y_line = self.x_plane_to_x_canvas(0)
        self.line((min_xc, y_x_line), (max_xc, y_x_line))
        self.line((x_y_line, min_yc), (x_y_line, max_yc))
        self.color = prev_color

    def draw_foreground(self):
        pass
