from typing import Any, Mapping

from typing_extensions import Self

from contexts.incidents.emergencies_counter_per_user.domain.entities.emergencies_counter_per_user_incremented_domain_event import (
    EmergenciesCounterPerUserIncrementedDomainEvent,
)
from contexts.incidents.emergencies_counter_per_user.domain.value_objects.emergencies_counter_per_user_total import (
    EmergenciesCounterPerUserTotal,
)
from contexts.incidents.shared.domain.value_objects import UserId
from contexts.shared.domain.aggregate import AggregateRoot


class EmergenciesCounterPerUser(AggregateRoot):
    def __init__(
        self,
        user_id: UserId,
        total: EmergenciesCounterPerUserTotal,
    ):
        super().__init__()
        self.user_id = user_id
        self.total = total

    @classmethod
    def initialize(cls, user_id: UserId) -> Self:
        return cls(user_id, EmergenciesCounterPerUserTotal.initialize())

    def record_incremented_event(self) -> None:
        self.record(
            EmergenciesCounterPerUserIncrementedDomainEvent(
                aggregate_id=self.user_id.value, data=dict(total=self.total.value)
            )
        )

    def to_primitives(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id.value,
            "total": self.total.value,
        }

    @classmethod
    def from_primitives(cls, data: Mapping[str, Any]) -> Self:
        return cls(
            user_id=data["_id"], total=EmergenciesCounterPerUserTotal(data["total"])
        )
