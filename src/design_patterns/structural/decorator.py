"""Decorator: 元のオブジェクトを包んで、機能を後から重ねていく。

題材: 文字列の表示に「枠」「左右の飾り」を重ねる。
包む側も包まれる側も同じ Display なので、何重にでも重ねられる。
（Python の @デコレーター構文とは別物だが、「関数を包んで機能を足す」という考え方は同じ）
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Display(ABC):
    @abstractmethod
    def lines(self) -> list[str]: ...

    def show(self) -> str:
        return "\n".join(self.lines())


class StringDisplay(Display):
    def __init__(self, text: str):
        self.text = text

    def lines(self) -> list[str]:
        return [self.text]


class Border(Display):
    """飾りの共通部分。中身（Display）を持つ。"""

    def __init__(self, inner: Display):
        self.inner = inner


class SideBorder(Border):
    def __init__(self, inner: Display, char: str):
        super().__init__(inner)
        self.char = char

    def lines(self) -> list[str]:
        return [f"{self.char}{line}{self.char}" for line in self.inner.lines()]


class FullBorder(Border):
    def lines(self) -> list[str]:
        inner = self.inner.lines()
        width = max(len(line) for line in inner)
        edge = "+" + "-" * width + "+"
        return [edge, *[f"|{line.ljust(width)}|" for line in inner], edge]
