from typing_extensions import Self

from contexts.shared.domain.value_objects import PositiveInteger


class EmergenciesCounterTotal(PositiveInteger):
    def increment(self) -> Self:
        return self.__class__(self.value + 1)

    @classmethod
    def initialize(cls) -> Self:
        return cls(0)
