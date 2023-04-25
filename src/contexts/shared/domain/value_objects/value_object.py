from typing import Generic, TypeVar

T = TypeVar("T")


class ValueObject(Generic[T]):
    def __init__(self, value: T):
        self._validate(value)
        self._value = value

    def _validate(self, value: T) -> None:
        pass

    @property
    def value(self) -> T:
        return self._value

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return self.value == other.value
