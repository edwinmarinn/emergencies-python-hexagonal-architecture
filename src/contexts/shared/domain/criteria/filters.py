import json
from functools import reduce
from typing import List

from typing_extensions import Self

from ..collection import Collection
from .filter import Filter, FilterDict


class Filters(Collection[Filter]):
    def __init__(self, filters: List[Filter]):
        super().__init__(filters)

    @classmethod
    def from_values(cls, values: List[FilterDict]) -> Self:
        return cls(list(map(lambda v: Filter.from_values(v), values)))

    @classmethod
    def from_json_str(cls, values: str):
        if values == "":
            values = "[]"
        _values = json.loads(values)
        if type(_values) != list:
            raise ValueError("The vales should be a valid JSON list")
        return cls.from_values(_values)

    def add(self, filter_: Filter) -> Self:
        filters = self.items + [filter_]
        return self.__class__(filters)

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
