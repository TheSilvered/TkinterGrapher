from core.grapher_base import FunctionGraph


class LineType1(FunctionGraph):
    def get_param_string(self):
        return "y = $m$x + $q$"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, m, q):
        return m * x + q
