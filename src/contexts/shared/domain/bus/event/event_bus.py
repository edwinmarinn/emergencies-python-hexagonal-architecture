from abc import ABC, abstractmethod
from typing import Iterable

from contexts.shared.domain.bus.event import DomainEvent
from contexts.shared.domain.bus.event import DomainEventSubscriber


class EventBus(ABC):
    @abstractmethod
    async def publish(self, *events: DomainEvent) -> None:
        pass

    def add_subscribers(self, subscribers: Iterable[DomainEventSubscriber]):
        pass
