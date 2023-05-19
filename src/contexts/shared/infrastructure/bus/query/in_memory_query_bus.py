from typing import Type

from contexts.shared.domain.bus.query import (
    Query,
    QueryBus,
    QueryHandler,
    QueryNotRegisteredError,
    Response,
)
from contexts.shared.infrastructure.bus.callable_first_parameter_extractor import (
    CallableFirstParameterExtractor,
)


def map_query_to_handlers(
    query_handlers: list[QueryHandler],
) -> dict[Type[Query], QueryHandler]:
    handlers: dict[Type[Query], QueryHandler] = {
        CallableFirstParameterExtractor.extract(handler): handler
        for handler in query_handlers
    }
    return handlers


class InMemoryQueryBus(QueryBus):
    def __init__(self, query_handlers: list[QueryHandler]):
        self.handlers = map_query_to_handlers(query_handlers)

    async def ask(self, query: Query) -> Response | None:
        handler = self.handlers.get(type(query))
        if handler is None:
            raise QueryNotRegisteredError(query)
        response: Response = await handler(query)
        return response
