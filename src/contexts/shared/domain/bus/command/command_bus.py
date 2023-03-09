from abc import ABC, abstractmethod

from .command import Command


class CommandBus(ABC):
    @abstractmethod
    async def dispatch(self, command: Command) -> None:
        pass
