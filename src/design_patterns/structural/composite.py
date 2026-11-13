"""Composite: 「入れ物」と「中身」を同じように扱う。

題材: ファイルとディレクトリ。ディレクトリの中にはファイルもディレクトリも入れられ、
どちらにも同じように size() や tree() を呼べる。
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Entry(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def tree(self, indent: int = 0) -> list[str]: ...


class File(Entry):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    def size(self) -> int:
        return self._size

    def tree(self, indent: int = 0) -> list[str]:
        return [f"{'  ' * indent}{self.name} ({self._size})"]


class Directory(Entry):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: list[Entry] = []

    def add(self, entry: Entry) -> Directory:
        self.children.append(entry)
        return self

    def size(self) -> int:
        return sum(child.size() for child in self.children)  # 中身が何かは気にしない

    def tree(self, indent: int = 0) -> list[str]:
        lines = [f"{'  ' * indent}{self.name}/ ({self.size()})"]
        for child in self.children:
            lines += child.tree(indent + 1)
        return lines
