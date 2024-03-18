from core.grapher_base import FunctionGraph
from math import sin


class Sine(FunctionGraph):
    def get_param_string(self):
        return "y = $a$sin($w$(x + $phi$)) + $b$"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, w, phi, b):
        return a * sin(w * x + phi) + b
