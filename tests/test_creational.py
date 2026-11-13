import threading

import pytest

from design_patterns.creational import abstract_factory, builder, factory_method, prototype, singleton


class TestSingleton:
    def setup_method(self):
        singleton.Database._reset_for_test()

    def test_何度生成しても同じインスタンス(self):
        a, b = singleton.Database(), singleton.Database()
        a.execute("SELECT 1")
        assert a is b
        assert b.queries == ["SELECT 1"]

    def test_複数スレッドから同時に生成しても1つだけ(self):
        results = []
        threads = [threading.Thread(target=lambda: results.append(singleton.Database())) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len({id(r) for r in results}) == 1


def test_factory_method_工場ごとに作る製品が変わり_共通の手順は親が持つ():
    cars, ships = factory_method.CarFactory(), factory_method.ShipFactory()

    assert cars.create("佐藤").use() == "佐藤 の車で道路を走る"
    assert ships.create("鈴木").use() == "鈴木 の船で海を進む"
    assert cars.owners == ["佐藤"] and ships.owners == ["鈴木"]


def test_abstract_factory_工場を差し替えるだけで出力形式が変わる():
    html = abstract_factory.build_link_page(abstract_factory.HtmlFactory())
    md = abstract_factory.build_link_page(abstract_factory.MarkdownFactory())

    assert html.startswith("<h1>リンク集</h1><ul><li>ニュース<ul>")
    assert '<a href="https://www.google.com/">Google</a>' in html
    assert md.splitlines() == [
        "# リンク集", "",
        "- ニュース", "  - [NHK](https://www.nhk.or.jp/)",
        "- 検索", "  - [Google](https://www.google.com/)",
    ]


@pytest.mark.parametrize("builder_cls, expected", [
    (builder.SanmaSetBuilder, "さんま定食（さんまの塩焼き・冷奴・味噌汁・ご飯）1000円"),
    (builder.PastaSetBuilder, "パスタセット（ナポリタン・サラダ・パン）1100円"),
])
def test_builder_同じ手順でも_builderによって出来上がりが変わる(builder_cls, expected):
    assert builder.Director(builder_cls()).construct().describe() == expected


class TestPrototype:
    def setup_method(self):
        self.manager = prototype.Manager()
        self.manager.register("strong", prototype.UnderlinePen("~"))
        self.manager.register("box", prototype.MessageBox("*"))

    def test_登録名で取り出してコピーを使う(self):
        assert self.manager.create("strong").use("Hello") == "Hello\n~~~~~"
        assert self.manager.create("box").use("Hi") == "******\n* Hi *\n******"

    def test_取り出したものは見本とは別のインスタンス(self):
        a, b = self.manager.create("box"), self.manager.create("box")
        a.decochar = "#"
        assert a is not b
        assert b.decochar == "*"

    def test_未登録の名前はKeyError(self):
        with pytest.raises(KeyError, match="登録されていない"):
            self.manager.create("unknown")
