"""Singleton: インスタンスを 1 つだけにする。

題材: アプリ全体で共有するデータベース接続。
Python ではモジュール自体が 1 回しか読み込まれないので、多くの場合はモジュール変数で十分。
ここではクラスとして書く場合の、__new__ を使う方法とスレッドセーフにする方法を示す。
"""
from __future__ import annotations

import threading


class Database:
    """何度生成しても同じインスタンスが返る。"""

    _instance: Database | None = None
    _lock = threading.Lock()

    def __new__(cls) -> Database:
        if cls._instance is None:
            with cls._lock:  # 複数スレッドから同時に呼ばれても 1 つしか作らない
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance.queries = []
                    cls._instance = instance
        return cls._instance

    def execute(self, sql: str) -> None:
        self.queries.append(sql)

    @classmethod
    def _reset_for_test(cls) -> None:
        cls._instance = None
