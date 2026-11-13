"""Command: 「やりたいこと」をオブジェクトにして、記録・取り消し・差し替えをできるようにする。

題材: 家電のリモコン。ボタンにコマンドを割り当て、押した履歴をもとに取り消し（undo）もできる。
リモコンは家電の操作方法を知らず、コマンドの execute / undo を呼ぶだけ。
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class Device:
    def __init__(self, name: str):
        self.name = name
        self.is_on = False


class Command(ABC):
    @abstractmethod
    def execute(self) -> str: ...

    @abstractmethod
    def undo(self) -> str: ...


class NoCommand(Command):
    """何も割り当てられていないボタン用（None チェックを書かずに済む）。"""

    def execute(self): return "何もしない"
    def undo(self): return "何もしない"


class PowerOnCommand(Command):
    def __init__(self, device: Device):
        self.device = device

    def execute(self):
        self.device.is_on = True
        return f"{self.device.name}をつけた"

    def undo(self):
        self.device.is_on = False
        return f"{self.device.name}を消した"


class PowerOffCommand(Command):
    def __init__(self, device: Device):
        self.device = device

    def execute(self):
        self.device.is_on = False
        return f"{self.device.name}を消した"

    def undo(self):
        self.device.is_on = True
        return f"{self.device.name}をつけた"


class RemoteController:
    def __init__(self, slots: int = 3):
        self._on = [NoCommand()] * slots
        self._off = [NoCommand()] * slots
        self._history: list[Command] = []

    def set_command(self, slot: int, on: Command, off: Command) -> None:
        self._on[slot], self._off[slot] = on, off

    def press_on(self, slot: int) -> str:
        return self._run(self._on[slot])

    def press_off(self, slot: int) -> str:
        return self._run(self._off[slot])

    def press_undo(self) -> str:
        return self._history.pop().undo() if self._history else "取り消す操作がありません"

    def _run(self, command: Command) -> str:
        self._history.append(command)
        return command.execute()
