"""Bridge: 「機能の階層」と「実装の階層」を分けて、それぞれ独立に増やせるようにする。

題材: 図形（長方形・正方形）と、その出力方法（テキスト・Markdown の表）。
図形 2 種 × 出力 2 種を継承で作ると 4 クラス必要だが、分ければ足し算で済む。
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Shape(ABC):
    """実装の階層: 形の情報を持つ。"""

    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def size(self) -> tuple[int, int]: ...

    def area(self) -> int:
        w, h = self.size()
        return w * h


class Rectangle(Shape):
    def __init__(self, width: int, height: int):
        self.width, self.height = width, height

    def name(self): return "長方形"
    def size(self): return (self.width, self.height)


class Square(Shape):
    def __init__(self, side: int):
        self.side = side

    def name(self): return "正方形"
    def size(self): return (self.side, self.side)


class ShapeWriter(ABC):
    """機能の階層: Shape を受け取って（橋渡しして）出力する。"""

    def __init__(self, shape: Shape):
        self.shape = shape

    @abstractmethod
    def write(self) -> str: ...


class TextWriter(ShapeWriter):
    def write(self) -> str:
        w, h = self.shape.size()
        return f"{self.shape.name()}: 幅 {w} × 高さ {h}（面積 {self.shape.area()}）"


class MarkdownTableWriter(ShapeWriter):
    def write(self) -> str:
        w, h = self.shape.size()
        return "\n".join([
            "| 図形 | 幅 | 高さ | 面積 |",
            "|---|---:|---:|---:|",
            f"| {self.shape.name()} | {w} | {h} | {self.shape.area()} |",
        ])
