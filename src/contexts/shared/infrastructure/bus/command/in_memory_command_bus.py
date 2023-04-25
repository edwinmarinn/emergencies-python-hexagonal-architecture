from typing import Dict, List, Type

from contexts.shared.domain.bus.command import (
    Command,
    CommandBus,
    CommandHandler,
    CommandNotRegisteredError,
)
from contexts.shared.infrastructure.bus.callable_first_parameter_extractor import (
    CallableFirstParameterExtractor,
)


def map_command_to_handlers(
    command_handlers: List[CommandHandler],
) -> Dict[Type[Command], CommandHandler]:
    handlers: Dict[Type[Command], CommandHandler] = {
        CallableFirstParameterExtractor.extract(handler): handler
        for handler in command_handlers
    }
    return handlers


class InMemoryCommandBus(CommandBus):
    def __init__(self, command_handlers: List[CommandHandler]):
        self.handlers = map_command_to_handlers(command_handlers)

    async def dispatch(self, command: Command) -> None:
        handler = self.handlers.get(type(command))
        if not handler:
            raise CommandNotRegisteredError(command)
        return await handler(command)
