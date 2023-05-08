from contexts.incidents.emergencies_counter.domain.entities import (
    EmergenciesCounter,
    EmergenciesCounterRepository,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId


class InMemoryEmergenciesCounterRepository(EmergenciesCounterRepository):
    def __init__(self):
        self._counter: EmergenciesCounter | None = None
        self._emergencies_id: set[EmergencyId] = set()

    async def increment(
        self, counter: EmergenciesCounter, emergency_id: EmergencyId
    ) -> EmergenciesCounter:
        self._emergencies_id.add(emergency_id)
        self._counter = EmergenciesCounter(
            id=counter.id, total=counter.total.increment()
        )
        return self._counter

    async def has_incremented(self, emergency_id: EmergencyId) -> bool:
        return emergency_id in self._emergencies_id

    async def search(self) -> EmergenciesCounter | None:
        return self._counter
