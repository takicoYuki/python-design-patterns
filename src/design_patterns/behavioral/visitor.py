"""Visitor: データ構造と、それに対する処理を分ける。

題材: 買い物かご。商品（本・果物）のクラスはそのままで、
「合計金額の計算」「送料の計算」のような処理を Visitor として後から追加できる。
"""
from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass


class Item(ABC):
    @abstractmethod
    def accept(self, visitor: Visitor) -> int: ...


@dataclass
class Book(Item):
    title: str
    price: int

    def accept(self, visitor):
        return visitor.visit_book(self)


@dataclass
class Fruit(Item):
    name: str
    price_per_kg: int
    weight_kg: float

    def accept(self, visitor):
        return visitor.visit_fruit(self)


class Visitor(ABC):
    @abstractmethod
    def visit_book(self, book: Book) -> int: ...

    @abstractmethod
    def visit_fruit(self, fruit: Fruit) -> int: ...


class PriceVisitor(Visitor):
    """1,000 円以上の本は 10% 引き。果物は重さで計算。"""

    def visit_book(self, book):
        return int(book.price * 0.9) if book.price >= 1000 else book.price

    def visit_fruit(self, fruit):
        return round(fruit.price_per_kg * fruit.weight_kg)


class ShippingVisitor(Visitor):
    """本は 1 冊 100 円、果物は 1kg あたり 300 円（端数切り上げ）。"""

    def visit_book(self, book):
        return 100

    def visit_fruit(self, fruit):
        return 300 * math.ceil(fruit.weight_kg)


def total(items: list[Item], visitor: Visitor) -> int:
    return sum(item.accept(visitor) for item in items)
