# from application import Application

# app = Application()
# app.run()

from core.turtle_canvas import TurtleCanvas
from core.param_input import TerminalParamInput
from core.grapher_base import FunctionGraph
import math
import turtle as t


class FunctionInClass(FunctionGraph):
    def get_param_string(self) -> str:
        return ""

    def get_func(self):
        return self.f

    @staticmethod
    def f(x):
        return (math.sin(math.pi*x/2) + math.cos(x)**2) / 2 - math.sqrt(3)


canvas = TurtleCanvas()
grapher = FunctionInClass(canvas, None, TerminalParamInput)

t.screensize(500, 500)
t.speed(0)
t.showturtle()
canvas.draw_background()
grapher.graph()
t.done()
