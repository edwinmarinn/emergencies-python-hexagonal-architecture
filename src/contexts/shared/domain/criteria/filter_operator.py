from contexts.shared.domain.value_objects.enum import Enum


class FilterOperator(Enum):
    EQUAL = '='
    NOT_EQUAL = '!='
    GT = '>'
    GTE = '>='
    LT = '<'
    LTE = '<='
    CONTAINS = 'CONTAINS'
    NOT_CONTAINS = 'NOT_CONTAINS'

    def is_containing(self) -> bool:
        return self in _containing

    @property
    def value(self) -> str:
        return self._value_


_containing = [FilterOperator.CONTAINS, FilterOperator.NOT_CONTAINS]
