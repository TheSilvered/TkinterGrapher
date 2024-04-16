from core.grapher_base import FunctionGraph
from math import sin


class Sine(FunctionGraph):
    @staticmethod
    def get_param_string():
        return "y = $a$sin($w$(x + $p$)) + $b$"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, w, p, b):
        return a * sin(w * x + p) + b
