from abc import ABC, abstractmethod

from contexts.shared.domain.bus.command import Command


class CommandHandler(ABC):
    pass

    @abstractmethod
    async def __call__(self, command: Command) -> None:
        pass
