from functools import reduce
from typing import List

from ..collection import Collection
from .filter import Filter, FilterDict


class Filters(Collection[Filter]):
    def __init__(self, filters: List[Filter]):
        super().__init__(filters)

    @classmethod
    def from_values(cls, values: List[FilterDict]) -> "Filters":
        return cls(list(map(lambda v: Filter.from_values(v), values)))

    def add(self, filter_: Filter) -> "Filters":
        filters = self.items + [filter_]
        return Filters(filters)

    @property
    def filters(self) -> List[Filter]:
        return self.items

    def serialize(self) -> str:
        return reduce(
            lambda acc, filter_: f"{acc}^{filter_.serialize()}",
            self.items,
            "",
        )

    def type(self):
        return Filter
