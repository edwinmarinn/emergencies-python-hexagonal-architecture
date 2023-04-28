from abc import ABC, abstractmethod

from contexts.shared.domain.bus.event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    async def publish(self, *events: DomainEvent) -> None:
        pass
