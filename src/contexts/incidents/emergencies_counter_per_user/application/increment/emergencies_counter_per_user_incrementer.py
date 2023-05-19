from contexts.incidents.emergencies_counter_per_user.domain.entities import (
    EmergenciesCounterPerUser,
    EmergenciesCounterPerUserRepository,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.event import EventBus


class EmergenciesCounterPerUserIncrementer:
    def __init__(self, repository: EmergenciesCounterPerUserRepository, bus: EventBus):
        self._repository = repository
        self._bus = bus

    async def __call__(self, user_id: UserId, emergency_id: EmergencyId) -> None:
        if not await self._repository.has_incremented(emergency_id=emergency_id):
            counter = await self._repository.increment(
                user_id=user_id, emergency_id=emergency_id
            )

            counter.record_incremented_event()
            await self._bus.publish(*counter.pull_domain_events())
