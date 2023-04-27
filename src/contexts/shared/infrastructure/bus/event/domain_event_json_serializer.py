import json

from contexts.shared.domain.bus.event import DomainEvent


class DomainEventJsonSerializer:
    @staticmethod
    def serialize(domain_event: DomainEvent) -> str:
        return json.dumps(
            {
                "data": {
                    "id": domain_event.event_id,
                    "type": domain_event.event_name(),
                    "occurred_on": domain_event.occurred_on,
                    "attributes": {
                        **domain_event.to_primitives(),
                        "id": domain_event.aggregate_id,
                    },
                },
                "meta": {},
            }
        )
