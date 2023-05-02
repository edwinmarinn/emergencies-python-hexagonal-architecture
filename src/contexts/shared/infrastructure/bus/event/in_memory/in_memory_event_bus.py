from collections import defaultdict
from typing import Dict, List, Type

from contexts.shared.domain.bus.event import (
    DomainEvent,
    DomainEventSubscriber,
    EventBus,
)

MapSubscribers = Dict[Type[DomainEvent], List[DomainEventSubscriber]]


def map_event_to_subscribers(
    event_subscribers: List[DomainEventSubscriber],
) -> MapSubscribers:
    map_subscribers: MapSubscribers = defaultdict(list)

    for subscriber in event_subscribers:
        for domain_event_type in subscriber.subscribed_to():
            map_subscribers[domain_event_type].append(subscriber)

    return map_subscribers


class InMemoryEventBus(EventBus):
    def __init__(self, event_subscribers: List[DomainEventSubscriber]):
        self.map_subscribers = map_event_to_subscribers(event_subscribers)

    async def publish(self, *events: DomainEvent) -> None:
        for event in events:
            subscribers = self.map_subscribers[type(event)]
            for subscriber in subscribers:
                await subscriber(event)
