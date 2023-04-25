from contexts.shared.domain.bus.event import DomainEvent, EventBus


class InMemoryEventBus(EventBus):
    def publish(self, *events: DomainEvent) -> None:
        pass
