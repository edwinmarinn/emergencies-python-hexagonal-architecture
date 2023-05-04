from typing import List

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
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.shared.domain.aggregate import AggregateRoot


class EmergenciesCounter(AggregateRoot):
    def __init__(
        self,
        id: EmergenciesCounterId,
        total: EmergenciesCounterTotal,
        existing_emergencies: List[EmergencyId] | None = None,
    ):
        super().__init__()
        self.id = id
        self.total = total
        self.existing_emergencies: List[EmergencyId] = existing_emergencies or []

    @classmethod
    def initialize(cls, id: EmergenciesCounterId) -> Self:
        return cls(id, EmergenciesCounterTotal.initialize())

    def increment(self, emergency_id: EmergencyId) -> None:
        self.total = self.total.increment()
        self.existing_emergencies.append(emergency_id)

        self.record(
            EmergenciesCounterIncrementedDomainEvent(
                aggregate_id=emergency_id.value, data=dict(total=self.total.value)
            )
        )

    def has_incremented(self, emergency_id: EmergencyId) -> bool:
        exists = emergency_id in self.existing_emergencies
        return exists
