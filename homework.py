import math
import turtle as t

from core.turtle_canvas import TurtleCanvas
from core.param_input import TerminalParamInput
from core.grapher_base import FunctionGraphX


class FunctionInClass(FunctionGraphX):
    @staticmethod
    def get_param_string() -> str:
        return ""

    def get_func(self):
        return self.f

    @staticmethod
    def f(x):
        return (math.sin(math.pi*x/2) + math.cos(x)**2) / 2 - math.sqrt(3)


def main():
    canvas = TurtleCanvas()
    grapher = FunctionInClass(canvas, TerminalParamInput)
    canvas.x_range = -5, 5
    canvas.y_range = -5, 5

    t.screensize(500, 500)
    t.speed(0)
    t.showturtle()
    canvas.draw_background()
    canvas.color = "#DD0000"
    canvas.line_width = 2
    grapher.graph()
    t.done()


if __name__ == "__main__":
    main()
