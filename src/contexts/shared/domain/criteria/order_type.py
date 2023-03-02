from contexts.shared.domain.value_objects.enum import Enum


class OrderType(Enum):
    ASC = 'asc'
    DESC = 'desc'
    NONE = 'none'

    @property
    def is_none(self) -> bool:
        return self == OrderType.NONE

    @property
    def value(self) -> str:
        return self._value_
