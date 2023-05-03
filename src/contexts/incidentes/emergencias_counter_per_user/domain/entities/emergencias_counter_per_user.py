from typing import List

from typing_extensions import Self

from contexts.incidentes.emergencias_counter_per_user.domain.entities.emergencias_counter_per_user_incremented_domain_event import (
    EmergenciasCounterPerUserIncrementedDomainEvent,
)
from contexts.incidentes.emergencias_counter_per_user.domain.value_objects.emergencias_counter_per_user_total import (
    EmergenciasCounterPerUserTotal,
)
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.incidentes.shared.domain.value_objects import UserId
from contexts.shared.domain.aggregate import AggregateRoot


class EmergenciasCounterPerUser(AggregateRoot):
    def __init__(
        self,
        user_id: UserId,
        total: EmergenciasCounterPerUserTotal,
        existing_emergencias: List[EmergenciaId] | None = None,
    ):
        super().__init__()
        self.user_id = user_id
        self.total = total
        self.existing_emergencias: List[EmergenciaId] = existing_emergencias or []

    @classmethod
    def initialize(cls, user_id: UserId) -> Self:
        return cls(user_id, EmergenciasCounterPerUserTotal.initialize())

    def increment(self, emergencia_id: EmergenciaId) -> None:
        self.total = self.total.increment()
        self.existing_emergencias.append(emergencia_id)

        self.record(
            EmergenciasCounterPerUserIncrementedDomainEvent(
                aggregate_id=emergencia_id.value, data=dict(total=self.total.value)
            )
        )

    def has_incremented(self, emergencia_id: EmergenciaId) -> bool:
        exists = emergencia_id in self.existing_emergencias
        return exists
