from contexts.shared.domain import DomainError
from contexts.shared.domain.bus.command import Command


class CommandNotRegisteredError(DomainError):
    def __init__(self, command: Command):
        self._command = command
        super().__init__()

    def error_code(self) -> str:
        return "command_bus_not_registered_error"

    def error_message(self) -> str:
        return f"The command <{type(self._command).__name__}> has not been registered"
