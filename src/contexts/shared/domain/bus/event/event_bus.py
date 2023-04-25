from abc import ABC, abstractmethod

from contexts.shared.domain.bus.event import DomainEvent


class EventBus(ABC):
    @abstractmethod
    def publish(self, *events: DomainEvent) -> None:
        pass
