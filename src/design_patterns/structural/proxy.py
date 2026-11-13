"""Proxy: 本物の代わりに受け付けて、必要になったときだけ本物に任せる。

題材: 時間のかかる外部 API の呼び出し。プロキシが結果をキャッシュし、
同じ引数なら本物を呼ばずに返す。使う側は本物かプロキシかを区別しない。
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class WeatherApi(ABC):
    @abstractmethod
    def forecast(self, city: str) -> str: ...


class RealWeatherApi(WeatherApi):
    """本物（実際には通信する想定）。呼ばれた回数を数えておく。"""

    def __init__(self, data: dict[str, str]):
        self._data = data
        self.calls = 0

    def forecast(self, city: str) -> str:
        self.calls += 1
        return self._data.get(city, "不明")


class CachingWeatherApi(WeatherApi):
    def __init__(self, real: WeatherApi):
        self._real = real
        self._cache: dict[str, str] = {}

    def forecast(self, city: str) -> str:
        if city not in self._cache:
            self._cache[city] = self._real.forecast(city)
        return self._cache[city]
