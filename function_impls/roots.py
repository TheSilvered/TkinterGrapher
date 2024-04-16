from core.grapher_base import FunctionGraphX


class SquareRoot(FunctionGraphX):
    @staticmethod
    def get_param_string():
        return "y = $a$sqrt($b$(x + $c$)) + $d$"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, b, c, d):
        return a * (b * (x + c))**0.5 + d


class NthRoot(FunctionGraphX):
    @staticmethod
    def get_param_string():
        return "y = $a$root$n$($b$(x + $c$)) + $d$"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, a, n, b, c, d):
        return a * (b * (x + c))**(1 / n) + d
