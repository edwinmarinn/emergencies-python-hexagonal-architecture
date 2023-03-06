from abc import ABC

from .query import Query
from .response import Response


class QueryBus(ABC):
    def ask(self, query: Query) -> Response | None:
        pass
