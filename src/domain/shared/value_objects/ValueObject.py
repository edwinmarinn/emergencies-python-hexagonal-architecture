import dataclasses
from typing import TypeVar, Generic

T = TypeVar("T")


@dataclasses.dataclass(frozen=True)
class ValueObject(Generic[T]):
    value: T
