from abc import ABC

from contexts.shared.domain.bus.event import DomainEvent


class EventBus(ABC):
    def publish(self, *events: DomainEvent) -> None:
        pass
