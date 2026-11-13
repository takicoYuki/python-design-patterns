import gc

from design_patterns.structural import adapter, bridge, composite, decorator, facade, flyweight, proxy


def test_adapter_既存クラスを変更せずにCSV出力のインターフェースに合わせる():
    model = adapter.UserModel()
    model.add_user("田中", 30)
    model.add_user("山田, 花子", 25)

    assert adapter.export(adapter.UserModelCsvAdapter(model)) == 'name,age\n田中,30\n"山田, 花子",25\n'


def test_bridge_図形と出力方法を自由に組み合わせられる():
    assert bridge.TextWriter(bridge.Rectangle(3, 4)).write() == "長方形: 幅 3 × 高さ 4（面積 12）"
    assert bridge.MarkdownTableWriter(bridge.Square(5)).write().splitlines()[-1] == "| 正方形 | 5 | 5 | 25 |"


def test_composite_ファイルとディレクトリを同じように扱える():
    root = composite.Directory("root")
    bin_dir = composite.Directory("bin").add(composite.File("vi", 100)).add(composite.File("latex", 200))
    root.add(bin_dir).add(composite.File("readme.txt", 50)).add(composite.Directory("tmp"))

    assert root.size() == 350
    assert root.tree() == [
        "root/ (350)", "  bin/ (300)", "    vi (100)", "    latex (200)", "  readme.txt (50)", "  tmp/ (0)",
    ]


def test_decorator_飾りを何重にでも重ねられる():
    plain = decorator.StringDisplay("Hello")
    assert plain.show() == "Hello"
    assert decorator.SideBorder(plain, "#").show() == "#Hello#"
    assert decorator.FullBorder(decorator.SideBorder(plain, "#")).show() == "+-------+\n|#Hello#|\n+-------+"


def test_facade_窓口に頼むだけで手順どおりに処理される():
    cook = facade.Cook()
    assert cook.make_french_fries() == ["じゃがいもを切る", "じゃがいもを揚げる", "塩をふる"]
    assert cook.make_salad()[0] == "ブロッコリーをゆでる"


class TestFlyweight:
    def test_同じ引数なら同じインスタンスを返す(self):
        a, b, c = flyweight.User("taro"), flyweight.User("taro"), flyweight.User("hanako")
        assert a is b
        assert a is not c

    def test_クラスごとに別々に管理する(self):
        user, car = flyweight.User("x"), flyweight.Car("x", "y")
        assert flyweight.Car("x", "y") is car
        assert user is not car

    def test_使われなくなったインスタンスは自動で解放される(self):
        before = flyweight.User.pool_size()
        temp = flyweight.User("temporary")
        assert flyweight.User.pool_size() == before + 1
        del temp
        gc.collect()
        assert flyweight.User.pool_size() == before


def test_proxy_同じ問い合わせは本物を呼ばずにキャッシュから返す():
    real = proxy.RealWeatherApi({"東京": "晴れ", "大阪": "雨"})
    api = proxy.CachingWeatherApi(real)

    assert [api.forecast("東京"), api.forecast("東京"), api.forecast("大阪")] == ["晴れ", "晴れ", "雨"]
    assert real.calls == 2
