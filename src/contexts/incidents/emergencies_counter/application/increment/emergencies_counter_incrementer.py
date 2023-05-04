from contexts.incidents.emergencies_counter.domain.entities.emergencies_counter import (
    EmergenciesCounter,
)
from contexts.incidents.emergencies_counter.domain.entities.emergencies_counter_repository import (
    EmergenciesCounterRepository,
)
from contexts.incidents.emergencies_counter.domain.value_objects.emergencies_counter_id import (
    EmergenciesCounterId,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.shared.domain.bus.event import EventBus


class EmergenciesCounterIncrementer:
    def __init__(self, repository: EmergenciesCounterRepository, bus: EventBus):
        self._repository = repository
        self._bus = bus

    async def __call__(self, emergency_id: EmergencyId):
        counter = (await self._repository.search()) or self.initialize_counter()

        if not counter.has_incremented(emergency_id):
            counter.increment(emergency_id)

            await self._repository.save(counter)
            await self._bus.publish(*counter.pull_domain_events())

    @staticmethod
    def initialize_counter() -> EmergenciesCounter:
        return EmergenciesCounter.initialize(EmergenciesCounterId.random())
