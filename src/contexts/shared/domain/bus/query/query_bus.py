from abc import ABC
from typing import Optional

from .query import Query
from .response import Response


class QueryBus(ABC):
    def ask(self, query: Query) -> Optional[Response]:
        pass

