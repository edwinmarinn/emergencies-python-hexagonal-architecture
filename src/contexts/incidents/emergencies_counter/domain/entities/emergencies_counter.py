from typing import Any, Mapping

from typing_extensions import Self

from contexts.incidents.emergencies_counter.domain.entities.emergencies_counter_incremented_domain_event import (
    EmergenciesCounterIncrementedDomainEvent,
)
from contexts.incidents.emergencies_counter.domain.value_objects.emergencies_counter_id import (
    EmergenciesCounterId,
)
from contexts.incidents.emergencies_counter.domain.value_objects.emergencies_counter_total import (
    EmergenciesCounterTotal,
)
from contexts.shared.domain.aggregate import AggregateRoot


class EmergenciesCounter(AggregateRoot):
    def __init__(self, id: EmergenciesCounterId, total: EmergenciesCounterTotal):
        super().__init__()
        self.id = id
        self.total = total

    @classmethod
    def initialize(cls, id: EmergenciesCounterId) -> Self:
        return cls(id, EmergenciesCounterTotal.initialize())

    def record_incremented_event(self) -> None:
        self.record(
            EmergenciesCounterIncrementedDomainEvent(
                aggregate_id=self.id.value, data=dict(total=self.total.value)
            )
        )

    def to_primitives(self) -> dict[str, Any]:
        return {
            "id": self.id.value,
            "total": self.total.value,
        }

    @classmethod
    def from_primitives(cls, data: Mapping[str, Any]) -> Self:
        return cls(
            id=EmergenciesCounterId(data.get("id") or data["_id"]),
            total=EmergenciesCounterTotal(data["total"]),
        )
