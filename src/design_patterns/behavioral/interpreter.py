"""Interpreter: 小さな言語の文法をクラスで表し、構文木をたどって実行する。

題材: 電卓のミニ言語。文法は次のとおり（BNF）。演算子の優先順位はなく、左から順に計算する。

    <program> ::= program <number> { <op> <number> } end
    <op>      ::= plus | minus | times | divide
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from fractions import Fraction


class ParseError(Exception):
    pass


class Context:
    """字句（トークン）を 1 つずつ読み進める。"""

    def __init__(self, text: str):
        self._tokens = text.split()
        self._pos = 0

    def current(self) -> str | None:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def skip(self, token: str) -> None:
        if self.current() != token:
            raise ParseError(f"{token} が必要ですが {self.current()} がありました")
        self._pos += 1

    def next_number(self) -> Fraction:
        token = self.current()
        try:
            value = Fraction(token)
        except (TypeError, ValueError):
            raise ParseError(f"数値が必要ですが {token} がありました") from None
        self._pos += 1
        return value


class Node(ABC):
    @abstractmethod
    def evaluate(self, acc: Fraction) -> Fraction: ...


class OperationNode(Node):
    OPS = {
        "plus": lambda a, b: a + b,
        "minus": lambda a, b: a - b,
        "times": lambda a, b: a * b,
        "divide": lambda a, b: a / b,
    }

    def __init__(self, op: str, operand: Fraction):
        if op == "divide" and operand == 0:
            raise ParseError("0 では割れません")
        self.op, self.operand = op, operand

    def evaluate(self, acc: Fraction) -> Fraction:
        return self.OPS[self.op](acc, self.operand)


class ProgramNode(Node):
    def __init__(self, context: Context):
        context.skip("program")
        self.start = context.next_number()
        self.operations: list[OperationNode] = []
        while context.current() in OperationNode.OPS:
            op = context.current()
            context.skip(op)
            self.operations.append(OperationNode(op, context.next_number()))
        context.skip("end")
        if context.current() is not None:
            raise ParseError(f"end の後に余分な {context.current()} があります")

    def evaluate(self, acc: Fraction = Fraction(0)) -> Fraction:
        value = self.start
        for node in self.operations:
            value = node.evaluate(value)
        return value


def run(source: str) -> Fraction:
    return ProgramNode(Context(source)).evaluate()
