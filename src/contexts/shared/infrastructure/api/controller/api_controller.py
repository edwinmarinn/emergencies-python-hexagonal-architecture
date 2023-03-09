from abc import ABC, abstractmethod
from typing import Dict

from contexts.shared.domain.bus.command import Command, CommandBus
from contexts.shared.domain.bus.query import Query, QueryBus, Response
from contexts.shared.infrastructure.api.exception import (
    ApiExceptionsHttpStatusCodeMapping,
)


class ApiController(ABC):
    def __init__(
        self,
        query_bus: QueryBus,
        command_bus: CommandBus,
        exception_handler: ApiExceptionsHttpStatusCodeMapping,
    ) -> None:
        self._query_bus = query_bus
        self._command_bus = command_bus
        self._exception_handler = exception_handler
        self._register_exceptions()

    @abstractmethod
    def exceptions(self) -> Dict[str, int]:
        pass

    async def dispatch(self, command: Command) -> None:
        await self._command_bus.dispatch(command)

    async def ask(self, query: Query) -> Response | None:
        return await self._query_bus.ask(query)

    def _register_exceptions(self) -> None:
        for exception, http_code in self.exceptions().items():
            self._exception_handler.register(exception, http_code)
