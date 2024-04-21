from typing import Callable
from core import FunctionGraphX, FunctionGraphY, FunctionInput, InputBase


class FunctionX(FunctionGraphX):
    @staticmethod
    def get_params() -> InputBase:
        return FunctionInput("f(x)")

    def get_func(self) -> Callable:
        return self.f

    def f(self, x):
        return self.params[x]


class FunctionY(FunctionGraphY):
    @staticmethod
    def get_params() -> InputBase:
        return FunctionInput("f(y)")

    def get_func(self) -> Callable:
        return self.f

    def f(self, y):
        return self.params[y]
