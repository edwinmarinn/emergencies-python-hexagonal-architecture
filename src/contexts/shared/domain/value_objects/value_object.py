from typing import Generic, TypeVar

T = TypeVar("T")


class ValueObject(Generic[T]):

    def __init__(self, value: T):
        self._validate(value)
        self._value = value

    def _validate(self, value: T):
        pass

    @property
    def value(self):
        return self._value
