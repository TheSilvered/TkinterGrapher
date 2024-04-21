from core import FunctionGraphX, ParamInput, InputBase


class NthRoot(FunctionGraphX):
    @staticmethod
    def get_params() -> InputBase:
        return ParamInput("y = rt$n$($a$ * x)")

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, n, a):
        return (a * x)**(1 / n)
