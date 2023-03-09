from abc import ABC, abstractmethod

from .query import Query
from .response import Response


class QueryHandler(ABC):
    @abstractmethod
    async def __call__(self, query: Query) -> Response:
        pass
