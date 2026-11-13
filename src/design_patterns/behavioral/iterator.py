"""Iterator: 集合の中身を、内部構造を知らずに 1 つずつ取り出す。

題材: 本棚。教科書どおりの Iterator クラスを書く方法と、
Python らしくジェネレーターで __iter__ を書く方法の 2 通りを並べている。
"""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    title: str


class BookShelfIterator(Iterator[Book]):
    """教科書どおりの書き方。位置を自分で管理する。"""

    def __init__(self, shelf: BookShelf):
        self._shelf = shelf
        self._index = 0

    def __next__(self) -> Book:
        if self._index >= len(self._shelf):
            raise StopIteration
        book = self._shelf.book_at(self._index)
        self._index += 1
        return book


class BookShelf:
    def __init__(self) -> None:
        self._books: list[Book] = []

    def append(self, book: Book) -> None:
        self._books.append(book)

    def book_at(self, index: int) -> Book:
        return self._books[index]

    def __len__(self) -> int:
        return len(self._books)

    def __iter__(self) -> Iterator[Book]:
        return BookShelfIterator(self)

    def reversed_titles(self) -> Iterator[str]:
        """Python らしい書き方。yield を使えば Iterator クラスを書かなくてよい。"""
        for i in range(len(self._books) - 1, -1, -1):
            yield self._books[i].title
