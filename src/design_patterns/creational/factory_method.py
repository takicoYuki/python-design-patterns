"""Factory Method: 何を作るかをサブクラスに任せる。

題材: 乗り物工場。共通の手順（製造 → 登録）は親クラスが持ち、
どの乗り物を作るかだけを CarFactory / ShipFactory が決める。
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Product(ABC):
    def __init__(self, owner: str):
        self.owner = owner

    @abstractmethod
    def use(self) -> str:
        ...


class Car(Product):
    def use(self) -> str:
        return f"{self.owner} の車で道路を走る"


class Ship(Product):
    def use(self) -> str:
        return f"{self.owner} の船で海を進む"


class Factory(ABC):
    def __init__(self) -> None:
        self.owners: list[str] = []

    def create(self, owner: str) -> Product:
        """テンプレートとなる手順。生成そのものは _create_product に任せる。"""
        product = self._create_product(owner)
        self.owners.append(owner)
        return product

    @abstractmethod
    def _create_product(self, owner: str) -> Product:
        ...


class CarFactory(Factory):
    def _create_product(self, owner: str) -> Product:
        return Car(owner)


class ShipFactory(Factory):
    def _create_product(self, owner: str) -> Product:
        return Ship(owner)
