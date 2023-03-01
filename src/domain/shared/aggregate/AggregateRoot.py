from typing import List

from domain.shared.bus.event.DomainEvent import DomainEvent


class AggregateRoot:
    def __init__(self) -> None:
        self.domain_events: List[DomainEvent] = []

    def pull_domain_events(self) -> List[DomainEvent]:
        domain_events = self.domain_events
        self.domain_events = []

        return domain_events

    def record(self, domain_event: DomainEvent) -> None:
        self.domain_events.append(domain_event)
