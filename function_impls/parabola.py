from core.grapher_base import FunctionGraphX


class Parabola(FunctionGraphX):
    @staticmethod
    def get_param_string():
        return "y = $a$x^2 + $b$x + $c$"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, b, c):
        return a * x * x + b * x + c
