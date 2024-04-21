from core import FunctionGraphX, ParamInput, InputBase


class Parabola(FunctionGraphX):
    @staticmethod
    def get_params() -> InputBase:
        return ParamInput("y = $a$x^2 + $b$x + $c$")

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, b, c):
        return a * x * x + b * x + c
