"""Strategy: アルゴリズム（戦略）を差し替えられるようにする。

題材: じゃんけん。Player は「次に何を出すか」を Strategy に任せる。
- WinningStreakStrategy: 勝ったら同じ手、負けたらランダム
- ProbabilityStrategy: 過去の勝敗から、勝ちやすかった手を出しやすくする
"""
from __future__ import annotations

import random
from abc import ABC, abstractmethod
from enum import Enum


class Hand(Enum):
    ROCK = 0      # グー
    SCISSORS = 1  # チョキ
    PAPER = 2     # パー

    def beats(self, other: Hand) -> bool:
        return (self.value + 1) % 3 == other.value

    def fight(self, other: Hand) -> int:
        """勝ち 1・あいこ 0・負け -1"""
        if self is other:
            return 0
        return 1 if self.beats(other) else -1


class Strategy(ABC):
    @abstractmethod
    def next_hand(self) -> Hand: ...

    @abstractmethod
    def study(self, my_hand: Hand, won: bool) -> None: ...


class WinningStreakStrategy(Strategy):
    def __init__(self, rng: random.Random):
        self._rng = rng
        self._won = False
        self._prev = Hand.ROCK

    def next_hand(self) -> Hand:
        if not self._won:
            self._prev = self._rng.choice(list(Hand))
        return self._prev

    def study(self, my_hand, won):
        self._won = won


class ProbabilityStrategy(Strategy):
    def __init__(self, rng: random.Random):
        self._rng = rng
        self._weights = {h: 1 for h in Hand}

    def next_hand(self) -> Hand:
        hands = list(self._weights)
        return self._rng.choices(hands, weights=[self._weights[h] for h in hands])[0]

    def study(self, my_hand, won):
        if won:
            self._weights[my_hand] += 1


class FixedStrategy(Strategy):
    """テストや比較用。いつも同じ手を出す。"""

    def __init__(self, hand: Hand):
        self.hand = hand

    def next_hand(self): return self.hand
    def study(self, my_hand, won): pass


class Player:
    def __init__(self, name: str, strategy: Strategy):
        self.name = name
        self.strategy = strategy
        self.wins = self.losses = self.draws = 0

    def play_against(self, other: Player) -> int:
        mine, theirs = self.strategy.next_hand(), other.strategy.next_hand()
        result = mine.fight(theirs)
        self.strategy.study(mine, result == 1)
        other.strategy.study(theirs, result == -1)
        self._count(result)
        other._count(-result)
        return result

    def _count(self, result: int) -> None:
        if result == 1:
            self.wins += 1
        elif result == -1:
            self.losses += 1
        else:
            self.draws += 1
