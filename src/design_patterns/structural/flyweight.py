"""Flyweight: 同じ内容のインスタンスを共有して、メモリを節約する。

題材: ユーザー。同じ名前で何度生成しても、作られるインスタンスは 1 つだけ。
WeakValueDictionary を使うので、どこからも使われなくなったものは自動で解放される。
"""
from __future__ import annotations

import weakref


class FlyweightMixin:
    """これを継承したクラスは、同じ引数での生成時に既存のインスタンスを返す。"""

    _pool: weakref.WeakValueDictionary

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._pool = weakref.WeakValueDictionary()  # クラスごとに別のプールを持つ

    def __new__(cls, *args):
        instance = cls._pool.get(args)
        if instance is None:
            instance = super().__new__(cls)
            cls._pool[args] = instance
        return instance

    @classmethod
    def pool_size(cls) -> int:
        return len(cls._pool)


class User(FlyweightMixin):
    def __init__(self, name: str):
        self.name = name


class Car(FlyweightMixin):
    def __init__(self, maker: str, model: str):
        self.maker, self.model = maker, model
