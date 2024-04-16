from core.grapher_base import FunctionGraph
from math import log


class Logarithm(FunctionGraph):
    @staticmethod
    def get_param_string():
        return "y = $a$log_$n$($b$(x + $c$)) + $d$"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, n, b, c, d):
        return a * log(b * (x + c), n) + d
