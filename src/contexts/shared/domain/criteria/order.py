from typing import Optional

from .order_by import OrderBy
from .order_type import OrderType


class Order:
    def __init__(self, order_by: OrderBy, order_type: OrderType):
        self._order_by = order_by
        self._order_type = order_type

    @property
    def order_by(self):
        return self._order_by

    @property
    def order_type(self):
        return self._order_type

    @property
    def is_none(self) -> bool:
        return self._order_type.is_none

    def serialize(self) -> str:
        return f"{self._order_by.value}.{self._order_type.value}"

    @classmethod
    def create_desc(cls, order_by: OrderBy) -> 'Order':
        return cls(order_by, OrderType.DESC)

    @classmethod
    def from_values(cls, order_by: Optional[str], order: Optional[str]) -> 'Order':
        if order_by is None:
            return cls.none()
        return cls(OrderBy(order_by), OrderType(order))

    @classmethod
    def none(cls) -> 'Order':
        return cls(OrderBy(''), OrderType.NONE)
