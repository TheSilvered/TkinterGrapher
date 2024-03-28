import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from typing import Any


class ParamInputBase(ABC):
    def __init__(self, layout: str, window: tk.Tk):
        self.layout = layout
        self.window = window
        self._params: dict[str, Any] = {}
        blocks = self.layout.split("$")
        for i in range(1, len(blocks), 2):
            self._params[blocks[i]] = None

    def get_names(self):
        return tuple(self._params.keys())

    @abstractmethod
    def available(self) -> bool:
        pass

    @abstractmethod
    def build_widget(self, parent: tk.Widget | tk.Tk) -> tk.Widget:
        pass

    @abstractmethod
    def _extract_value(self, param_name: str, param_value: Any) -> int | float | None:
        pass

    def __getitem__(self, item):
        val: Any = self._params.get(item)
        if val is None:
            return None
        return self._extract_value(item, val)


class ParamInput(ParamInputBase):
    def available(self) -> bool:
        for param in self._params:
            if self[param] is None:
                return False
        return True

    def build_widget(self, parent) -> tk.Widget:
        blocks = self.layout.split("$")
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
        return tk.Label(parent, text=self.layout)

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
