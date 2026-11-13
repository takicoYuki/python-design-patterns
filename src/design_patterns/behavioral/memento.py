"""Memento: オブジェクトの状態を保存しておき、あとで元に戻せるようにする。

題材: テキストエディター。保存した状態（Memento）の中身は Editor だけが読み書きし、
履歴を管理する History は中身を知らずに預かるだけ（カプセル化を壊さない）。
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Memento:
    _text: str
    _cursor: int


class Editor:
    def __init__(self) -> None:
        self.text = ""
        self.cursor = 0

    def type(self, s: str) -> None:
        self.text = self.text[: self.cursor] + s + self.text[self.cursor:]
        self.cursor += len(s)

    def save(self) -> Memento:
        return Memento(self.text, self.cursor)

    def restore(self, memento: Memento) -> None:
        self.text, self.cursor = memento._text, memento._cursor


class History:
    """Caretaker（世話役）。Memento の中身には触らない。"""

    def __init__(self, editor: Editor):
        self._editor = editor
        self._stack: list[Memento] = []

    def backup(self) -> None:
        self._stack.append(self._editor.save())

    def undo(self) -> bool:
        if not self._stack:
            return False
        self._editor.restore(self._stack.pop())
        return True
