from typing import List, Type

from contexts.incidentes.emergencias.domain.entities import EmergenciaCreatedDomainEvent
from contexts.incidentes.emergencias_counter.application.increment.emergencias_counter_incrementer import (
    EmergenciasCounterIncrementer,
)
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.shared.domain.bus.event import DomainEvent, DomainEventSubscriber


class IncrementEmergenciasCounterOnEmergenciaCreated(DomainEventSubscriber):
    def __init__(self, incrementer: EmergenciasCounterIncrementer):
        self._incrementer = incrementer

    @staticmethod
    def subscribed_to() -> List[Type[DomainEvent]]:
        return [EmergenciaCreatedDomainEvent]

    async def __call__(self, event: EmergenciaCreatedDomainEvent):
        emergencia_id = EmergenciaId(event.aggregate_id)
        await self._incrementer(emergencia_id)
