from abc import ABC, abstractmethod
from typing import Any

from tkinter import ttk
import tkinter as tk

from .function_parser import parse_func, FuncAST, ParseFuncError


class InputBase(ABC):
    def __init__(self, fmt: str):
        self.fmt = fmt

    @abstractmethod
    def get_names(self):
        pass

    @abstractmethod
    def available(self) -> bool:
        pass

    @abstractmethod
    def build_widget(self, parent: tk.Widget | tk.Tk) -> tk.Widget:
        pass

    @abstractmethod
    def __getitem__(self, item):
        pass


class ParamInputBase(InputBase, ABC):
    def __init__(self, fmt: str):
        super().__init__(fmt)
        self._params: dict[str, Any] = {}
        blocks = self.fmt.split("$")
        for i in range(1, len(blocks), 2):
            self._params[blocks[i]] = None

    def get_names(self):
        return tuple(self._params.keys())

    def __getitem__(self, item):
        val: Any = self._params.get(item)
        if val is None:
            return None
        return self._extract_value(item, val)

    @abstractmethod
    def _extract_value(self, param_name: str, param_value: Any) -> int | float | None:
        pass


class ParamInput(ParamInputBase):
    def available(self) -> bool:
        for param in self.get_names():
            if self[param] is None:
                return False
        return True

    def build_widget(self, parent) -> tk.Widget:
        blocks = self.fmt.split("$")
        frame = ttk.Frame(parent)

        for i, block in enumerate(blocks):
            if i % 2 == 1:
                entry = ttk.Entry(frame, width=4, justify="right")
                entry.grid(row=0, column=i)
                self._params[block] = entry
            else:
                label = ttk.Label(frame, text=block)
                label.grid(row=0, column=i)
        return frame

    def _extract_value(self, param_name, param_value):
        try:
            return float(param_value.get())
        except ValueError:
            return None


class TerminalParamInput(ParamInputBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for param in self.get_names():
            val = self.__get_val(param)
            self._params[param] = val

    def available(self) -> bool:
        return True

    def build_widget(self, parent: tk.Widget | tk.Tk) -> tk.Widget:
        return tk.Label(parent, text=self.fmt.replace("$", ""))

    @staticmethod
    def __get_val(name):
        while True:
            val = input(f"Insert value for {name!r}: ")
            try:
                val = float(val)
                return val
            except ValueError:
                print("Invalid input.")

    def _extract_value(self, param_name: str, param_value: Any) -> int | float | None:
        return param_value


class FunctionInput(InputBase):
    def __init__(self, var_name: str):
        super().__init__(var_name)
        param_name = var_name.removeprefix("f(").removesuffix(")")
        self.param_name: str = param_name
        self.parsed_string: str = ""
        self.current_ast: FuncAST | None = None
        self.func_entry: ttk.Entry | None = None

    def get_names(self):
        return []

    def __update_ast(self):
        if self.func_entry is None:
            return
        if self.func_entry.get() == self.parsed_string:
            return
        self.parsed_string = self.func_entry.get()
        new_ast = parse_func(self.parsed_string, self.param_name)
        if isinstance(new_ast, ParseFuncError):
            self.current_ast = None
        else:
            self.current_ast = new_ast

    def available(self) -> bool:
        if self.func_entry is None:
            return False
        self.__update_ast()
        return self.current_ast is not None

    def build_widget(self, parent: tk.Widget | tk.Tk) -> tk.Widget:
        frame = ttk.Frame(parent)
        f_label = ttk.Label(frame, text=f"f({self.param_name}) =")
        f_label.grid(row=0, column=0)
        self.func_entry = ttk.Entry(frame, width=50)
        self.func_entry.grid(row=0, column=1)
        return frame

    def __getitem__(self, item: int | float) -> int | float | None:
        self.__update_ast()
        if self.current_ast is None:
            return None
        return self.current_ast.evaluate(item)
