from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

from .query import Query
from .response import Response

Q = TypeVar("Q", bound=Query)
R = TypeVar("R", bound=Response)


class QueryHandler(Generic[Q, R], ABC):
    @abstractmethod
    def subscribed_to(self) -> Type[Query]:
        pass

    @abstractmethod
    async def __call__(self, query: Q) -> R:
        pass
