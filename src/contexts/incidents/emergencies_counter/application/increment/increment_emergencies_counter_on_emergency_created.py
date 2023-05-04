from typing import List, Type

from contexts.incidents.emergencies.domain.entities import EmergencyCreatedDomainEvent
from contexts.incidents.emergencies_counter.application.increment.emergencies_counter_incrementer import (
    EmergenciesCounterIncrementer,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.shared.domain.bus.event import DomainEvent, DomainEventSubscriber


class IncrementEmergenciesCounterOnEmergencyCreated(DomainEventSubscriber):
    def __init__(self, incrementer: EmergenciesCounterIncrementer):
        self._incrementer = incrementer

    @staticmethod
    def subscribed_to() -> List[Type[DomainEvent]]:
        return [EmergencyCreatedDomainEvent]

    async def __call__(self, event: EmergencyCreatedDomainEvent):
        emergency_id = EmergencyId(event.aggregate_id)
        await self._incrementer(emergency_id)
