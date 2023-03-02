from typing import TypedDict

from .filter_field import FilterField
from .filter_operator import FilterOperator
from .filter_value import FilterValue


class FilterDict(TypedDict):
    field: str
    operator: str
    value: str


class Filter:
    def __init__(self, field: FilterField, operator: FilterOperator, value: FilterValue):
        self._field = field
        self._operator = operator
        self._value = value

    @classmethod
    def from_values(cls, values: FilterDict) -> "Filter":
        return cls(
            FilterField(values["field"]),
            FilterOperator(values["operator"]),
            FilterValue(values["value"]),
        )

    @property
    def field(self) -> FilterField:
        return self._field

    @property
    def operator(self) -> FilterOperator:
        return self._operator

    @property
    def value(self) -> FilterValue:
        return self._value

    def serialize(self) -> str:
        return f"{self.field.value}.{self.operator.value}.{self.value.value}"
