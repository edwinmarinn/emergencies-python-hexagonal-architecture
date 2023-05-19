from contexts.shared.domain.bus.event.domain_event import DomainEvent


class AggregateRoot:
    def __init__(self) -> None:
        self.domain_events: list[DomainEvent] = []

    def pull_domain_events(self) -> list[DomainEvent]:
        domain_events = self.domain_events
        self.domain_events = []

        return domain_events

    def record(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)
