from contexts.incidentes.emergencias_counter.domain.entities import (
    EmergenciasCounter,
    EmergenciasCounterRepository,
)


class InMemoryEmergenciasCounterRepository(EmergenciasCounterRepository):
    def __init__(self):
        self._data: EmergenciasCounter | None = None

    async def search(self) -> EmergenciasCounter | None:
        return self._data

    async def save(self, counter: EmergenciasCounter) -> None:
        self._data = counter
