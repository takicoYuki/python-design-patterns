"""Facade: 複数のクラスを組み合わせる手順を、1 つの窓口にまとめる。

題材: 料理。包丁・鍋・フライヤーの使い方と順番を知らなくても、Cook に頼めば完成品が出てくる。
"""
from __future__ import annotations


class Knife:
    def cut(self, ingredient: str) -> str:
        return f"{ingredient}を切る"


class Boiler:
    def boil(self, ingredient: str) -> str:
        return f"{ingredient}をゆでる"


class Fryer:
    def fry(self, ingredient: str) -> str:
        return f"{ingredient}を揚げる"


class Cook:
    """窓口。使う側は Cook の 1 メソッドだけを知っていればよい。"""

    def __init__(self) -> None:
        self.knife, self.boiler, self.fryer = Knife(), Boiler(), Fryer()

    def make_french_fries(self) -> list[str]:
        return [self.knife.cut("じゃがいも"), self.fryer.fry("じゃがいも"), "塩をふる"]

    def make_salad(self) -> list[str]:
        return [self.boiler.boil("ブロッコリー"), self.knife.cut("トマト"), "盛り付ける"]
