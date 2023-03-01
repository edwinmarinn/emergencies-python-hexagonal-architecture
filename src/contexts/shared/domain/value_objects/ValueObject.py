import dataclasses
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class ValueObject(Generic[T]):
    value: T
