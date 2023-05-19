from typing import Type

from contexts.incidents.emergencies.domain.entities import EmergencyCreatedDomainEvent
from contexts.incidents.emergencies_counter_per_user.application.increment.emergencies_counter_per_user_incrementer import (
    EmergenciesCounterPerUserIncrementer,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.event import DomainEvent, DomainEventSubscriber


class IncrementEmergenciesCounterPerUserOnEmergencyCreated(DomainEventSubscriber):
    def __init__(self, incrementer: EmergenciesCounterPerUserIncrementer):
        self._incrementer = incrementer

    @staticmethod
    def subscribed_to() -> list[Type[DomainEvent]]:
        return [EmergencyCreatedDomainEvent]

    async def __call__(self, event: EmergencyCreatedDomainEvent):
        emergency_id = EmergencyId(event.aggregate_id)
        data = event.to_primitives()
        user_id = UserId(data["user_id"])

        await self._incrementer(user_id=user_id, emergency_id=emergency_id)
