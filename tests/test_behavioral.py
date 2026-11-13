import random
from fractions import Fraction

import pytest

from design_patterns.behavioral import (
    chain_of_responsibility as cor, command, interpreter, iterator, mediator, memento, observer, state,
    strategy, template_method, visitor,
)


@pytest.mark.parametrize("user, expected", [
    (cor.User("田中", 20, "tanaka@example.com"), None),
    (cor.User(" ", 20, "x@example.com"), "名前が入力されていません"),
    (cor.User("田中", 17, "x@example.com"), "18 歳以上の方のみ登録できます"),
    (cor.User("田中", 20, "not-an-email"), "メールアドレスの形式が正しくありません"),
    (cor.User("", 10, "bad"), "名前が入力されていません"),  # 最初に見つかった問題だけを返す
])
def test_chain_of_responsibility_順番にチェックして最初の問題を返す(user, expected):
    assert cor.default_chain().handle(user) == expected


def test_command_ボタンにコマンドを割り当て_押した順に取り消せる():
    light, tv = command.Device("照明"), command.Device("テレビ")
    remote = command.RemoteController()
    remote.set_command(0, command.PowerOnCommand(light), command.PowerOffCommand(light))
    remote.set_command(1, command.PowerOnCommand(tv), command.PowerOffCommand(tv))

    assert remote.press_on(0) == "照明をつけた"
    assert remote.press_on(1) == "テレビをつけた"
    assert remote.press_off(0) == "照明を消した"
    assert remote.press_on(2) == "何もしない"
    assert (light.is_on, tv.is_on) == (False, True)

    remote.press_undo()  # 空きボタン
    assert remote.press_undo() == "照明をつけた"
    assert remote.press_undo() == "テレビを消した"
    assert light.is_on and not tv.is_on


class TestInterpreter:
    @pytest.mark.parametrize("source, expected", [
        ("program 10 end", 10),
        ("program 1 plus 2 times 3 end", 9),  # 優先順位はなく左から計算する
        ("program 10 minus 4 divide 3 end", 2),
        ("program 1 divide 3 end", Fraction(1, 3)),
    ])
    def test_ミニ言語を解析して計算する(self, source, expected):
        assert interpreter.run(source) == expected

    @pytest.mark.parametrize("source, message", [
        ("1 plus 2 end", "program が必要"),
        ("program 1 plus end", "数値が必要"),
        ("program 1 plus 2", "end が必要"),
        ("program 1 end extra", "余分な extra"),
        ("program 1 divide 0 end", "0 では割れません"),
    ])
    def test_文法の誤りはParseErrorにする(self, source, message):
        with pytest.raises(interpreter.ParseError, match=message):
            interpreter.run(source)


def test_iterator_内部構造を知らずに順番に取り出せる():
    shelf = iterator.BookShelf()
    for title in ["Around the World in 80 Days", "Bible", "Cinderella"]:
        shelf.append(iterator.Book(title))

    assert [b.title for b in shelf] == ["Around the World in 80 Days", "Bible", "Cinderella"]
    assert list(shelf.reversed_titles()) == ["Cinderella", "Bible", "Around the World in 80 Days"]
    assert [b.title for b in shelf] == [b.title for b in shelf]  # 何度でも最初から回せる


def test_mediator_画面同士の連携ルールは仲介役だけが持つ():
    m = mediator.WindowMediator()
    main, settings, help_ = (mediator.Window(n, m) for n in ("main", "settings", "help"))

    main.open()
    settings.open()
    help_.open()  # 設定は自動で閉じる
    assert (settings.is_open, help_.is_open) == (False, True)

    main.close()  # メインを閉じたら全部閉じる
    assert not any(w.is_open for w in m.windows.values())


def test_memento_保存した状態に戻せる():
    editor = memento.Editor()
    history = memento.History(editor)

    editor.type("Hello")
    history.backup()
    editor.type(", World")
    history.backup()
    editor.type("!!!")

    assert history.undo() and editor.text == "Hello, World"
    assert history.undo() and editor.text == "Hello"
    assert editor.cursor == 5
    assert history.undo() is False


def test_observer_変化を登録した相手全員に通知する():
    subject = observer.NumberSubject()
    digit, graph = observer.DigitObserver(), observer.GraphObserver()
    subject.attach(digit)
    subject.attach(graph)

    subject.run([3, 1])
    subject.detach(graph)
    subject.run([2])

    assert digit.output == ["DigitObserver: 3", "DigitObserver: 1", "DigitObserver: 2"]
    assert graph.output == ["GraphObserver: ***", "GraphObserver: *"]


def test_state_時刻によって状態が切り替わり_同じ操作でも対応が変わる():
    system = state.SafeSystem()
    system.set_clock(10)
    system.use_safe()
    system.set_clock(22)
    system.use_safe()
    system.alarm()

    assert system.logs == ["金庫使用（昼間）", "昼間 → 夜間"]
    assert system.calls == ["緊急事態: 夜間の金庫使用", "非常ベル（夜間）"]


class TestStrategy:
    def test_じゃんけんの勝ち負け(self):
        H = strategy.Hand
        assert H.ROCK.fight(H.SCISSORS) == 1
        assert H.SCISSORS.fight(H.PAPER) == 1
        assert H.PAPER.fight(H.ROCK) == 1
        assert H.ROCK.fight(H.PAPER) == -1
        assert H.ROCK.fight(H.ROCK) == 0

    def test_勝ったら同じ手を出し続ける戦略(self):
        streak = strategy.WinningStreakStrategy(random.Random(0))
        first = streak.next_hand()
        streak.study(first, won=True)
        assert all(streak.next_hand() is first for _ in range(5))

    def test_戦略を差し替えて対戦できる(self):
        rng = random.Random(42)
        a = strategy.Player("A", strategy.ProbabilityStrategy(rng))
        b = strategy.Player("B", strategy.FixedStrategy(strategy.Hand.ROCK))
        for _ in range(300):
            a.play_against(b)

        assert a.wins + a.losses + a.draws == 300
        assert (a.wins, a.losses) == (b.losses, b.wins)
        assert a.wins > a.losses  # グーしか出さない相手には、パーを出しやすく学習していく


def test_template_method_流れは共通で中身だけが違う():
    assert template_method.CharDisplay("H").display() == "<<HHHHH>>"
    assert template_method.StringDisplay("Hi").display() == "+--+\n" + "|Hi|\n" * 5 + "+--+\n"


def test_visitor_商品クラスを変えずに別の計算を追加できる():
    cart = [visitor.Book("Python 入門", 2000), visitor.Book("雑誌", 500), visitor.Fruit("りんご", 600, 1.5)]

    assert visitor.total(cart, visitor.PriceVisitor()) == 1800 + 500 + 900
    assert visitor.total(cart, visitor.ShippingVisitor()) == 100 + 100 + 600
