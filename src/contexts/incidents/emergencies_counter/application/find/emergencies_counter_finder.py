from contexts.incidents.emergencies_counter.domain.entities import (
    EmergenciesCounterRepository,
)


class EmergenciesCounterFinder:
    def __init__(self, repository: EmergenciesCounterRepository):
        self._repository = repository

    async def __call__(self) -> int:
        counter = await self._repository.search()
        if not counter:
            return 0

        return counter.total.value
