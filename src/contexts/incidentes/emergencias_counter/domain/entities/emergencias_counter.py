from typing import List

from typing_extensions import Self

from contexts.incidentes.emergencias_counter.domain.entities.emergencias_counter_incremented_domain_event import (
    EmergenciasCounterIncrementedDomainEvent,
)
from contexts.incidentes.emergencias_counter.domain.value_objects.emergencias_counter_id import (
    EmergenciasCounterId,
)
from contexts.incidentes.emergencias_counter.domain.value_objects.emergencias_counter_total import (
    EmergenciasCounterTotal,
)
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.shared.domain.aggregate import AggregateRoot


class EmergenciasCounter(AggregateRoot):
    def __init__(
        self,
        id: EmergenciasCounterId,
        total: EmergenciasCounterTotal,
        existing_emergencias: List[EmergenciaId] | None = None,
    ):
        super().__init__()
        self.id = id
        self.total = total
        self.existing_emergencias: List[EmergenciaId] = existing_emergencias or []

    @classmethod
    def initialize(cls, id: EmergenciasCounterId) -> Self:
        return cls(id, EmergenciasCounterTotal.initialize())

    def increment(self, emergencia_id: EmergenciaId) -> None:
        self.total = self.total.increment()
        self.existing_emergencias.append(emergencia_id)

        self.record(
            EmergenciasCounterIncrementedDomainEvent(
                aggregate_id=emergencia_id.value, data=dict(total=self.total.value)
            )
        )

    def has_incremented(self, emergencia_id: EmergenciaId) -> bool:
        exists = emergencia_id in self.existing_emergencias
        return exists
