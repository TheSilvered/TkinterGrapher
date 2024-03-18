import math
import turtle as t

from core.turtle_canvas import TurtleCanvas
from core.param_input import TerminalParamInput
from core.grapher_base import FunctionGraph


class FunctionInClass(FunctionGraph):
    def get_param_string(self) -> str:
        return ""

    def get_func(self):
        return self.f

    @staticmethod
    def f(x):
        return (math.sin(math.pi*x/2) + math.cos(x)**2) / 2 - math.sqrt(3)


def main():
    canvas = TurtleCanvas()
    grapher = FunctionInClass(canvas, None, TerminalParamInput)
    canvas.x_range = -5, 5
    canvas.y_range = -5, 5

    t.screensize(500, 500)
    t.speed(0)
    t.showturtle()
    canvas.draw_background()
    t.pencolor("#DD0000")
    t.pensize(2)
    grapher.graph()
    t.done()


if __name__ == "__main__":
    main()
