"""State: 状態をクラスで表し、状態ごとに違う振る舞いを if 文ではなくクラスの切り替えで表現する。

題材: 金庫の警備システム。昼と夜で、金庫を使ったときや非常ベルを押したときの対応が変わる。
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def use_safe(self, context: SafeSystem) -> None: ...

    @abstractmethod
    def alarm(self, context: SafeSystem) -> None: ...

    def on_clock(self, context: SafeSystem, hour: int) -> None:
        context.change_state(DAY if 9 <= hour < 17 else NIGHT)


class DayState(State):
    def use_safe(self, context): context.record("金庫使用（昼間）")
    def alarm(self, context): context.call_security("非常ベル（昼間）")

    def __str__(self): return "昼間"


class NightState(State):
    def use_safe(self, context): context.call_security("緊急事態: 夜間の金庫使用")
    def alarm(self, context): context.call_security("非常ベル（夜間）")

    def __str__(self): return "夜間"


# 状態は中身を持たないので、1 つずつ作って使い回す
DAY = DayState()
NIGHT = NightState()


class SafeSystem:
    def __init__(self) -> None:
        self.state: State = DAY
        self.logs: list[str] = []
        self.calls: list[str] = []

    def set_clock(self, hour: int) -> None:
        self.state.on_clock(self, hour)

    def change_state(self, state: State) -> None:
        if state is not self.state:
            self.logs.append(f"{self.state} → {state}")
            self.state = state

    def use_safe(self) -> None:
        self.state.use_safe(self)

    def alarm(self) -> None:
        self.state.alarm(self)

    def record(self, message: str) -> None:
        self.logs.append(message)

    def call_security(self, message: str) -> None:
        self.calls.append(message)
