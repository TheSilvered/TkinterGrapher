from core import FunctionGraphX


class NthRoot(FunctionGraphX):
    @staticmethod
    def get_param_string():
        return "y = rt$n$($a$ * x)"

    def get_func(self):
        return self.f

    @staticmethod
    def f(x, n, a):
        return (a * x)**(1 / n)
