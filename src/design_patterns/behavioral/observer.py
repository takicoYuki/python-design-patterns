"""Observer: 状態が変わったことを、登録している相手に通知する。

題材: 数を生成するもの（Subject）と、その数を表示するもの（数字表示・棒グラフ表示）。
Subject は通知先が何をするかを知らず、新しい表示方法も Subject を変えずに追加できる。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable


class Observer(ABC):
    @abstractmethod
    def update(self, number: int) -> None: ...


class NumberSubject:
    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self.number = 0

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def run(self, numbers: Iterable[int]) -> None:
        for n in numbers:
            self.number = n
            for observer in self._observers:
                observer.update(n)


class DigitObserver(Observer):
    def __init__(self) -> None:
        self.output: list[str] = []

    def update(self, number: int) -> None:
        self.output.append(f"DigitObserver: {number}")


class GraphObserver(Observer):
    def __init__(self) -> None:
        self.output: list[str] = []

    def update(self, number: int) -> None:
        self.output.append(f"GraphObserver: {'*' * number}")
