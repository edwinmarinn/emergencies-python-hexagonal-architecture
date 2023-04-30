import json

from contexts.shared.domain.bus.event import DomainEvent

from .domain_event_mapping import DomainEventMapping


class DomainEventJsonDeserializer:
    def __init__(self, domain_event_mapping: DomainEventMapping):
        self._domain_event_mapping = domain_event_mapping

    def deserialize(self, domain_event: str | bytes) -> DomainEvent:
        event_data = json.loads(domain_event)
        event_name = event_data["data"]["type"]
        event_class = self._domain_event_mapping.get(event_name)

        if event_class is None:
            raise RuntimeError(
                f"The event <{event_name}> doesn't exist or has no subscribers"
            )

        return event_class.from_primitives(
            aggregate_id=event_data["data"]["attributes"]["id"],
            data=event_data["data"]["attributes"],
            event_id=event_data["data"]["id"],
            occurred_on=event_data["data"]["occurred_on"],
        )
