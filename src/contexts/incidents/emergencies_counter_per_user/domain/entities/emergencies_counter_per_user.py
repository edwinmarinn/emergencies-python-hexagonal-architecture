from typing import List

from typing_extensions import Self

from contexts.incidents.emergencies_counter_per_user.domain.entities.emergencies_counter_per_user_incremented_domain_event import (
    EmergenciesCounterPerUserIncrementedDomainEvent,
)
from contexts.incidents.emergencies_counter_per_user.domain.value_objects.emergencies_counter_per_user_total import (
    EmergenciesCounterPerUserTotal,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId
from contexts.shared.domain.aggregate import AggregateRoot


class EmergenciesCounterPerUser(AggregateRoot):
    def __init__(
        self,
        user_id: UserId,
        total: EmergenciesCounterPerUserTotal,
        existing_emergencies: List[EmergencyId] | None = None,
    ):
        super().__init__()
        self.user_id = user_id
        self.total = total
        self.existing_emergencies: List[EmergencyId] = existing_emergencies or []

    @classmethod
    def initialize(cls, user_id: UserId) -> Self:
        return cls(user_id, EmergenciesCounterPerUserTotal.initialize())

    def increment(self, emergency_id: EmergencyId) -> None:
        self.total = self.total.increment()
        self.existing_emergencies.append(emergency_id)

        self.record(
            EmergenciesCounterPerUserIncrementedDomainEvent(
                aggregate_id=emergency_id.value, data=dict(total=self.total.value)
            )
        )

    def has_incremented(self, emergency_id: EmergencyId) -> bool:
        exists = emergency_id in self.existing_emergencies
        return exists
