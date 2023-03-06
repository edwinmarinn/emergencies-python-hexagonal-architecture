from abc import ABC, abstractmethod

from .command import Command


class CommandBus(ABC):
    @abstractmethod
    def dispatch(self, command: Command) -> None:
        pass
