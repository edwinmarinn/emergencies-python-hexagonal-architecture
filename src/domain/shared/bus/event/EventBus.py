from abc import ABC

from domain.shared.bus.event import DomainEvent


class EventBus(ABC):
    def publish(self, *events: DomainEvent) -> None:
        pass
