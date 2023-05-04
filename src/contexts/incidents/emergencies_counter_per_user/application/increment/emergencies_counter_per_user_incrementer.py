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
        counter = (await self._repository.search(user_id)) or self.initialize_counter(
            user_id
        )

        if not counter.has_incremented(emergency_id):
            counter.increment(emergency_id)

            await self._repository.save(counter)
            await self._bus.publish(*counter.pull_domain_events())

    @staticmethod
    def initialize_counter(user_id: UserId) -> EmergenciesCounterPerUser:
        return EmergenciesCounterPerUser.initialize(user_id)
