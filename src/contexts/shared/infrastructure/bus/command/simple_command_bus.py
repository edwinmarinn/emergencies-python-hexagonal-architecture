from typing import Dict, Type

from contexts.shared.domain.bus.command import Command, CommandBus, CommandHandler

from .command_not_registered_error import CommandNotRegisteredError


class SimpleCommandBus(CommandBus):
    def __init__(self):
        self.handlers: Dict[Type[Command], CommandHandler] = {}

    def register(self, query_class: Type[Command], handler: CommandHandler):
        self.handlers[query_class] = handler

    async def dispatch(self, command: Command) -> None:
        handler = self.handlers.get(type(command))
        if not handler:
            raise CommandNotRegisteredError(command)
        return await handler(command)
