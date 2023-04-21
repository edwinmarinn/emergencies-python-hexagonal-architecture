from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from contexts.shared.domain.bus.command import Command

C = TypeVar("C", bound=Command)


class CommandHandler(Generic[C], ABC):
    pass

    @abstractmethod
    async def __call__(self, command: C) -> None:
        pass
