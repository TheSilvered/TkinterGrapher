from core import FunctionGraphX
from math import sin, cos, tan


class Sine(FunctionGraphX):
    @staticmethod
    def get_param_string():
        return "y = $a$ * sin($w$ * x)"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, w):
        return a * sin(w * x)


class Cosine(FunctionGraphX):
    @staticmethod
    def get_param_string():
        return "y = $a$ * cos($w$ * x)"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, w):
        return a * cos(w * x)


class Tangent(FunctionGraphX):
    @staticmethod
    def get_param_string():
        return "y = $a$ * tan($w$ * x)"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, w):
        return a * tan(w * x)
