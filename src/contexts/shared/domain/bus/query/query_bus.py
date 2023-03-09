from abc import ABC, abstractmethod

from .query import Query
from .response import Response


class QueryBus(ABC):
    @abstractmethod
    async def ask(self, query: Query) -> Response | None:
        pass
