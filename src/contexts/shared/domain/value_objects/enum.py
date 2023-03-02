import random
import re
from abc import ABC, abstractmethod
from enum import Enum as EnumCore


class Enum(EnumCore):
    # _cache = {}

    @classmethod
    def from_string(cls, value):
        return cls(value)

    # @staticmethod
    # def values():
    #     cls = type.__qualname__
    #     if cls not in Enum._cache:
    #         Enum._cache[cls] = {k: v for k, v in cls.__dict__.items() if not k.startswith("_")}
    #     return Enum._cache[cls]

    # @staticmethod
    # def random_value():
    #     return random.choice(list(Enum.values().values()))

    # @classmethod
    # def random(cls):
    #     return cls(cls.random_value())

    # @staticmethod
    # def _keys_formatter():
    #     return lambda unused, key: re.sub(r"_(.)", lambda m: m.group(1).upper(), key.lower())

    def equals(self, other):
        return other == self

    def __str__(self):
        return str(self.value)
