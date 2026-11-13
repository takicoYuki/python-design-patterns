"""Chain of Responsibility: 処理できる担当者が見つかるまで、順番にたらい回しにする。

題材: 会員登録の入力チェック。名前 → 年齢 → メールアドレスの順にチェック役をつなぎ、
最初に見つかった問題を返す。チェック役の追加や順番の入れ替えは、つなぎ方を変えるだけでよい。
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int
    email: str


class Handler(ABC):
    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        """次の担当をつなぐ。戻り値を使って a.set_next(b).set_next(c) と書ける。"""
        self._next = handler
        return handler

    def handle(self, user: User) -> str | None:
        """問題があればメッセージを、なければ None を返す。"""
        error = self.check(user)
        if error is not None or self._next is None:
            return error
        return self._next.handle(user)

    @abstractmethod
    def check(self, user: User) -> str | None: ...


class NameCheck(Handler):
    def check(self, user):
        return None if user.name.strip() else "名前が入力されていません"


class AgeCheck(Handler):
    def __init__(self, minimum: int = 18):
        super().__init__()
        self.minimum = minimum

    def check(self, user):
        return None if user.age >= self.minimum else f"{self.minimum} 歳以上の方のみ登録できます"


class EmailCheck(Handler):
    def check(self, user):
        return None if re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", user.email) else "メールアドレスの形式が正しくありません"


def default_chain() -> Handler:
    head = NameCheck()
    head.set_next(AgeCheck()).set_next(EmailCheck())
    return head
