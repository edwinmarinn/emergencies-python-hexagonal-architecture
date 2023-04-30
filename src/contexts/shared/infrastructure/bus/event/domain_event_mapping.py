from functools import reduce
from typing import Dict, Type
from typing import Iterable

from contexts.shared.domain.bus.event import DomainEvent, DomainEventSubscriber

MapEventName = Dict[str, Type[DomainEvent]]


class DomainEventMapping:
    def __init__(self, subscribers: Iterable[DomainEventSubscriber]):
        self._mapping: MapEventName = reduce(self._events_extractor, subscribers, {})

    @staticmethod
    def _events_extractor(
        mapping: MapEventName, subscriber: DomainEventSubscriber
    ) -> MapEventName:
        mapping_local: MapEventName = {
            event_class.event_name(): event_class
            for event_class in subscriber.subscribed_to()
        }

        return {**mapping, **mapping_local}

    def __getitem__(self, event_name: str) -> Type[DomainEvent]:
        return self._mapping[event_name]

    def get(self, event_name: str) -> Type[DomainEvent] | None:
        if event_name not in self._mapping:
            return None

        return self._mapping[event_name]
