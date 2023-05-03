from typing import List, Type

from contexts.incidentes.emergencias.domain.entities import EmergenciaCreatedDomainEvent
from contexts.incidentes.emergencias_counter_per_user.application.increment.emergencias_counter_per_user_incrementer import (
    EmergenciasCounterPerUserIncrementer,
)
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.incidentes.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.event import DomainEvent, DomainEventSubscriber


class IncrementEmergenciasCounterPerUserOnEmergenciaCreated(DomainEventSubscriber):
    def __init__(self, incrementer: EmergenciasCounterPerUserIncrementer):
        self._incrementer = incrementer

    @staticmethod
    def subscribed_to() -> List[Type[DomainEvent]]:
        return [EmergenciaCreatedDomainEvent]

    async def __call__(self, event: EmergenciaCreatedDomainEvent):
        emergencia_id = EmergenciaId(event.aggregate_id)
        data = event.to_primitives()
        user_id = UserId(data["user_id"])

        await self._incrementer(user_id=user_id, emergencia_id=emergencia_id)
