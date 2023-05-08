from contexts.incidents.emergencies_counter.domain.entities import (
    EmergenciesCounter,
    EmergenciesCounterRepository,
)


class InMemoryEmergenciesCounterRepository(EmergenciesCounterRepository):
    def __init__(self):
        self._data: EmergenciesCounter | None = None

    async def save(self, counter: EmergenciesCounter) -> None:
        self._data = counter

    async def search(self) -> EmergenciesCounter | None:
        return self._data
