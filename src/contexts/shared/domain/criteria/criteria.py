from .filter import Filter
from .filters import Filters
from .order import Order


class Criteria:
    def __init__(
        self,
        filters: Filters,
        order: Order,
        offset: int | None = None,
        limit: int | None = None,
    ):
        self._filters = filters
        self._order = order
        self._offset = offset
        self._limit = limit

    @property
    def has_filters(self) -> bool:
        return self._filters.count > 0

    @property
    def has_order(self) -> bool:
        return not self._order.is_none

    @property
    def plain_filters(self) -> list[Filter]:
        return self._filters.filters

    @property
    def filters(self) -> Filters:
        return self._filters

    @property
    def order(self) -> Order:
        return self._order

    @property
    def offset(self) -> int | None:
        return self._offset

    @property
    def limit(self) -> int | None:
        return self._limit

    def serialize(self) -> str:
        return f"{self._filters.serialize()}~~{self._order.serialize()}~~{self._offset}~~{self._limit}"
