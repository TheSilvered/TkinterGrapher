from core import FunctionGraphX, ParamInput, InputBase
from math import log


class Logarithm(FunctionGraphX):
    @staticmethod
    def get_params() -> InputBase:
        return ParamInput("y = log_$n$($a$ * x)")

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, n, a):
        return log(a * x, n)
