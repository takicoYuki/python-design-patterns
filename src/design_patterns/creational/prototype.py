"""Prototype: 登録しておいた見本をコピーして新しいインスタンスを作る。

題材: 文字列の装飾（枠で囲む・下線を引く）。
クラス名ではなく登録名で取り出してコピーするので、使う側は具体的なクラスを知らなくてよい。
"""
from __future__ import annotations

import copy
from abc import ABC, abstractmethod


class Prototype(ABC):
    @abstractmethod
    def use(self, text: str) -> str: ...

    def clone(self) -> Prototype:
        return copy.deepcopy(self)


class MessageBox(Prototype):
    def __init__(self, decochar: str):
        self.decochar = decochar

    def use(self, text: str) -> str:
        line = self.decochar * (len(text) + 4)
        return f"{line}\n{self.decochar} {text} {self.decochar}\n{line}"


class UnderlinePen(Prototype):
    def __init__(self, ulchar: str):
        self.ulchar = ulchar

    def use(self, text: str) -> str:
        return f"{text}\n{self.ulchar * len(text)}"


class Manager:
    def __init__(self) -> None:
        self._showcase: dict[str, Prototype] = {}

    def register(self, name: str, prototype: Prototype) -> None:
        self._showcase[name] = prototype

    def create(self, name: str) -> Prototype:
        try:
            return self._showcase[name].clone()
        except KeyError:
            raise KeyError(f"登録されていない見本です: {name}") from None
