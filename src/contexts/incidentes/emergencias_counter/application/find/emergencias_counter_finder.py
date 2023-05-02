from contexts.incidentes.emergencias_counter.domain.entities import (
    EmergenciasCounterRepository,
)


class EmergenciasCounterFinder:
    def __init__(self, repository: EmergenciasCounterRepository):
        self._repository = repository

    async def __call__(self) -> int:
        counter = await self._repository.search()
        if not counter:
            return 0

        return counter.total.value
