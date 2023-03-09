from typing import Dict, Type

from contexts.shared.domain.bus.query import Query, QueryBus, QueryHandler, Response

from .query_not_registered_error import QueryNotRegisteredError


class SimpleQueryBus(QueryBus):
    def __init__(self):
        self.handlers: Dict[Type[Query], QueryHandler] = {}

    def register(self, query_class: Type[Query], handler: QueryHandler):
        self.handlers[query_class] = handler

    async def ask(self, query: Query) -> Response | None:
        handler = self.handlers.get(type(query))
        if handler is None:
            raise QueryNotRegisteredError(query)
        return await handler(query)
