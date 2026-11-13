"""Adapter: 既存のクラスを、求められているインターフェースに合わせる。

題材: ユーザー情報を持つ既存のモデルを、「CSV に書き出せるもの」として扱う。
UserModel 自体には手を入れず、間に UserModelCsvAdapter をはさむ。
"""
from __future__ import annotations

import csv
import io
from abc import ABC, abstractmethod
from collections.abc import Iterator


class UserModel:
    """既存のクラス（変更できない前提）。ヘッダーと行を別々に返す。"""

    def __init__(self) -> None:
        self._users: list[tuple[str, int]] = []

    def add_user(self, name: str, age: int) -> None:
        self._users.append((name, age))

    def load_headers(self) -> list[str]:
        return ["name", "age"]

    def yield_rows(self) -> Iterator[tuple[str, int]]:
        yield from self._users


class CsvWritable(ABC):
    """求められているインターフェース。"""

    @abstractmethod
    def write_csv(self, out: io.TextIOBase) -> None: ...


class UserModelCsvAdapter(CsvWritable):
    def __init__(self, model: UserModel):
        self._model = model

    def write_csv(self, out) -> None:
        writer = csv.writer(out, lineterminator="\n")
        writer.writerow(self._model.load_headers())
        writer.writerows(self._model.yield_rows())


def export(target: CsvWritable) -> str:
    """CsvWritable なら何でも受け取れる側のコード。"""
    buf = io.StringIO()
    target.write_csv(buf)
    return buf.getvalue()
