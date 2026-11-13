"""Template Method: 処理の流れ（テンプレート）は親クラスで決め、細部をサブクラスで書く。

題材: 文字や文字列を飾って 5 回表示する。open → print × 5 → close という流れは共通で、
それぞれの中身だけが CharDisplay と StringDisplay で違う。
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class AbstractDisplay(ABC):
    REPEAT = 5

    def display(self) -> str:
        """テンプレートメソッド。サブクラスでは上書きしない。"""
        parts = [self.open()]
        parts += [self.print() for _ in range(self.REPEAT)]
        parts.append(self.close())
        return "".join(parts)

    @abstractmethod
    def open(self) -> str: ...

    @abstractmethod
    def print(self) -> str: ...

    @abstractmethod
    def close(self) -> str: ...


class CharDisplay(AbstractDisplay):
    def __init__(self, ch: str):
        self.ch = ch

    def open(self): return "<<"
    def print(self): return self.ch
    def close(self): return ">>"


class StringDisplay(AbstractDisplay):
    def __init__(self, text: str):
        self.text = text

    def _line(self) -> str:
        return "+" + "-" * len(self.text) + "+\n"

    def open(self): return self._line()
    def print(self): return f"|{self.text}|\n"
    def close(self): return self._line()
