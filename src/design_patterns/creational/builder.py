"""Builder: 複雑なオブジェクトを手順に分けて組み立てる。

題材: 定食。Director（店員）は「主菜 → 副菜 → 汁物 → ご飯」という順番だけを知っていて、
何を載せるかは Builder（さんま定食・パスタセット）ごとに違う。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class SetMeal:
    name: str
    items: list[str] = field(default_factory=list)
    price: int = 0

    def describe(self) -> str:
        return f"{self.name}（{'・'.join(self.items)}）{self.price}円"


class SetMealBuilder(ABC):
    def __init__(self, name: str):
        self.meal = SetMeal(name)

    def _add(self, item: str, price: int) -> None:
        self.meal.items.append(item)
        self.meal.price += price

    @abstractmethod
    def main_dish(self) -> None: ...

    @abstractmethod
    def side_dish(self) -> None: ...

    def soup(self) -> None:  # 汁物がない定食もあるので、既定では何もしない
        pass

    @abstractmethod
    def staple(self) -> None: ...


class SanmaSetBuilder(SetMealBuilder):
    def __init__(self):
        super().__init__("さんま定食")

    def main_dish(self): self._add("さんまの塩焼き", 600)
    def side_dish(self): self._add("冷奴", 150)
    def soup(self): self._add("味噌汁", 100)
    def staple(self): self._add("ご飯", 150)


class PastaSetBuilder(SetMealBuilder):
    def __init__(self):
        super().__init__("パスタセット")

    def main_dish(self): self._add("ナポリタン", 800)
    def side_dish(self): self._add("サラダ", 200)
    def staple(self): self._add("パン", 100)


class Director:
    """組み立ての順番だけを知っている。"""

    def __init__(self, builder: SetMealBuilder):
        self.builder = builder

    def construct(self) -> SetMeal:
        self.builder.main_dish()
        self.builder.side_dish()
        self.builder.soup()
        self.builder.staple()
        return self.builder.meal
