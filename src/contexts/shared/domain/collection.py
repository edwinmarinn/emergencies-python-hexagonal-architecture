from collections.abc import Iterable, Iterator
from typing import Generic, List, Type, TypeVar

T = TypeVar("T")


class Collection(Iterable, Generic[T]):
    def __init__(self, items: List[T]):
        self._items = items
        self._assert_items_are_of_type()

    def __iter__(self) -> Iterator:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    def _assert_items_are_of_type(self):
        for item in self._items:
            if not isinstance(item, self.type()):
                raise TypeError(f"Expected instance of {self.type()}")

    def type(self) -> Type:
        raise NotImplementedError("type() method must be implemented in subclasses")

    @property
    def items(self) -> List[T]:
        return self._items

    @property
    def count(self) -> int:
        return len(self.items)
