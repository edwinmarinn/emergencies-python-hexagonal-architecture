from abc import ABC, abstractmethod
from typing import Iterable

from contexts.shared.domain.bus.event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    async def publish(self, events: Iterable[DomainEvent]) -> None:
        pass
