"""Abstract Factory: 関連する部品のセットをまとめて作る。

題材: リンク・リスト・ページからなるリンク集。
HTML 版と Markdown 版の工場を差し替えるだけで、組み立て側のコードは変えずに出力形式を変えられる。
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Item(ABC):
    def __init__(self, caption: str):
        self.caption = caption

    @abstractmethod
    def render(self) -> str:
        ...


class Link(Item):
    def __init__(self, caption: str, url: str):
        super().__init__(caption)
        self.url = url


class Tray(Item):
    def __init__(self, caption: str):
        super().__init__(caption)
        self.items: list[Item] = []

    def add(self, item: Item) -> Tray:
        self.items.append(item)
        return self


class Page(ABC):
    def __init__(self, title: str):
        self.title = title
        self.contents: list[Item] = []

    def add(self, item: Item) -> Page:
        self.contents.append(item)
        return self

    @abstractmethod
    def render(self) -> str:
        ...


class Factory(ABC):
    @abstractmethod
    def create_link(self, caption: str, url: str) -> Link: ...

    @abstractmethod
    def create_tray(self, caption: str) -> Tray: ...

    @abstractmethod
    def create_page(self, title: str) -> Page: ...


# --- HTML 版 ---
class HtmlLink(Link):
    def render(self) -> str:
        return f'<li><a href="{self.url}">{self.caption}</a></li>'


class HtmlTray(Tray):
    def render(self) -> str:
        inner = "".join(i.render() for i in self.items)
        return f"<li>{self.caption}<ul>{inner}</ul></li>"


class HtmlPage(Page):
    def render(self) -> str:
        inner = "".join(i.render() for i in self.contents)
        return f"<h1>{self.title}</h1><ul>{inner}</ul>"


class HtmlFactory(Factory):
    def create_link(self, caption, url): return HtmlLink(caption, url)
    def create_tray(self, caption): return HtmlTray(caption)
    def create_page(self, title): return HtmlPage(title)


# --- Markdown 版 ---
class MarkdownLink(Link):
    def render(self, depth: int = 0) -> str:
        return f"{'  ' * depth}- [{self.caption}]({self.url})"


class MarkdownTray(Tray):
    def render(self, depth: int = 0) -> str:
        lines = [f"{'  ' * depth}- {self.caption}"]
        lines += [i.render(depth + 1) for i in self.items]
        return "\n".join(lines)


class MarkdownPage(Page):
    def render(self) -> str:
        return "\n".join([f"# {self.title}", ""] + [i.render() for i in self.contents])


class MarkdownFactory(Factory):
    def create_link(self, caption, url): return MarkdownLink(caption, url)
    def create_tray(self, caption): return MarkdownTray(caption)
    def create_page(self, title): return MarkdownPage(title)


def build_link_page(factory: Factory) -> str:
    """どの工場でも同じ手順で組み立てられる（具体的なクラス名を知らない）。"""
    news = factory.create_tray("ニュース")
    news.add(factory.create_link("NHK", "https://www.nhk.or.jp/"))
    search = factory.create_tray("検索")
    search.add(factory.create_link("Google", "https://www.google.com/"))
    return factory.create_page("リンク集").add(news).add(search).render()
