# python-design-patterns

![CI](https://github.com/takicoYuki/python-design-patterns/actions/workflows/ci.yml/badge.svg)

GoF の **23 のデザインパターン** を Python で書いたサンプル集です。
各パターンを「身近な題材」で書き、使い方と効果をテストで確認できるようにしています。

デザインパターンの勉強のために書いていたコードを、次の方針で整理し直しました。

- 1 パターン 1 ファイル。冒頭のコメントに「何のためのパターンか」「題材」を書く
- `print` やファイル出力ではなく **戻り値** で結果を返し、テストで確認できるようにする
- Python らしい書き方がある場合は併記する（Iterator のジェネレーター、Flyweight の `WeakValueDictionary` など）

## パターン一覧

### 生成（オブジェクトの作り方）

| パターン | 題材 | ひとことで |
|---|---|---|
| [Singleton](src/design_patterns/creational/singleton.py) | データベース接続 | インスタンスを 1 つに。スレッドセーフに `__new__` で実装 |
| [Factory Method](src/design_patterns/creational/factory_method.py) | 車・船の工場 | 何を作るかをサブクラスに任せる |
| [Abstract Factory](src/design_patterns/creational/abstract_factory.py) | リンク集（HTML / Markdown） | 関連する部品のセットを工場ごと差し替える |
| [Builder](src/design_patterns/creational/builder.py) | 定食 | 組み立ての順番（Director）と中身（Builder）を分ける |
| [Prototype](src/design_patterns/creational/prototype.py) | 文字列の装飾 | 登録した見本をコピーして使う |

### 構造（クラスやオブジェクトの組み合わせ方）

| パターン | 題材 | ひとことで |
|---|---|---|
| [Adapter](src/design_patterns/structural/adapter.py) | ユーザー情報の CSV 出力 | 既存クラスを変えずにインターフェースを合わせる |
| [Bridge](src/design_patterns/structural/bridge.py) | 図形 × 出力形式 | 機能と実装の階層を分けて、掛け算を足し算にする |
| [Composite](src/design_patterns/structural/composite.py) | ファイルとディレクトリ | 入れ物と中身を同じように扱う |
| [Decorator](src/design_patterns/structural/decorator.py) | 文字列の枠飾り | 包んで機能を重ねる |
| [Facade](src/design_patterns/structural/facade.py) | 料理 | 複雑な手順を 1 つの窓口にまとめる |
| [Flyweight](src/design_patterns/structural/flyweight.py) | ユーザー・車 | 同じ内容のインスタンスを共有する |
| [Proxy](src/design_patterns/structural/proxy.py) | 天気 API | 代理で受けて、必要なときだけ本物を呼ぶ（キャッシュ） |

### 振る舞い（処理の分担や受け渡し方）

| パターン | 題材 | ひとことで |
|---|---|---|
| [Chain of Responsibility](src/design_patterns/behavioral/chain_of_responsibility.py) | 会員登録の入力チェック | 処理できる担当が見つかるまで順に回す |
| [Command](src/design_patterns/behavioral/command.py) | 家電のリモコン | 操作をオブジェクトにして、履歴と取り消しを可能にする |
| [Interpreter](src/design_patterns/behavioral/interpreter.py) | 電卓のミニ言語 | 文法をクラスで表して構文木を実行する |
| [Iterator](src/design_patterns/behavioral/iterator.py) | 本棚 | 内部構造を知らずに 1 つずつ取り出す |
| [Mediator](src/design_patterns/behavioral/mediator.py) | 設定・ヘルプ画面 | 部品同士の連携ルールを仲介役に集める |
| [Memento](src/design_patterns/behavioral/memento.py) | テキストエディターの元に戻す | 状態を保存して復元する |
| [Observer](src/design_patterns/behavioral/observer.py) | 数値と表示 | 変化を登録した相手に通知する |
| [State](src/design_patterns/behavioral/state.py) | 金庫の警備（昼・夜） | 状態ごとの振る舞いを if ではなくクラスで切り替える |
| [Strategy](src/design_patterns/behavioral/strategy.py) | じゃんけん | アルゴリズムを差し替える |
| [Template Method](src/design_patterns/behavioral/template_method.py) | 文字の繰り返し表示 | 流れは親、細部は子が決める |
| [Visitor](src/design_patterns/behavioral/visitor.py) | 買い物かごの金額・送料 | データ構造を変えずに処理を追加する |

## 例: Strategy

```python
import random
from design_patterns.behavioral.strategy import Hand, Player, ProbabilityStrategy, FixedStrategy

a = Player("A", ProbabilityStrategy(random.Random(42)))   # 勝った手を出しやすく学習する
b = Player("B", FixedStrategy(Hand.ROCK))                # いつもグー
for _ in range(300):
    a.play_against(b)
print(a.wins, a.losses, a.draws)  # 学習してパーを出しやすくなり、A が勝ち越す
```

## テスト

```bash
pip install pytest
pytest
```

パターンごとにテストを書いています（43 件）。CI では Python 3.10 と 3.13 で実行しています。

## このパターン集を使って作ったもの

- [javadoc-classifier](https://github.com/takicoYuki/javadoc-classifier) … Strategy・Factory・Facade などを実際のツールに当てはめたもの

## ライセンス

MIT
