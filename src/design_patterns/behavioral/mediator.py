"""Mediator: 部品同士が直接やりとりせず、仲介役を通して連携する。

題材: アプリの画面（メイン・設定・ヘルプ）。どの画面を開いたら何を閉じるかというルールを
仲介役（WindowMediator）だけが持つので、画面のクラス同士は互いを知らなくてよい。
"""
from __future__ import annotations


class Window:
    def __init__(self, name: str, mediator: WindowMediator):
        self.name = name
        self.is_open = False
        self._mediator = mediator
        mediator.register(self)

    def open(self) -> None:
        self.is_open = True
        self._mediator.notify(self, "opened")

    def close(self) -> None:
        self.is_open = False
        self._mediator.notify(self, "closed")


class WindowMediator:
    """ルール: 設定とヘルプは同時に開かない。メインを閉じたら全部閉じる。"""

    def __init__(self) -> None:
        self.windows: dict[str, Window] = {}
        self.log: list[str] = []

    def register(self, window: Window) -> None:
        self.windows[window.name] = window

    def notify(self, sender: Window, event: str) -> None:
        self.log.append(f"{sender.name} {event}")
        if event == "opened" and sender.name in ("settings", "help"):
            other = self.windows.get("help" if sender.name == "settings" else "settings")
            if other and other.is_open:
                other.close()
        if event == "closed" and sender.name == "main":
            for w in self.windows.values():
                if w.is_open:
                    w.close()
