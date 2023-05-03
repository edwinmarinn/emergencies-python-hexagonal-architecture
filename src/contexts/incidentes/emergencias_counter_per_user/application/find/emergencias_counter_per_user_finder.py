from contexts.incidentes.emergencias_counter_per_user.domain.entities import (
    EmergenciasCounterPerUserRepository,
)
from contexts.incidentes.shared.domain.value_objects import UserId


class EmergenciasCounterPerUserFinder:
    def __init__(self, repository: EmergenciasCounterPerUserRepository):
        self._repository = repository

    async def __call__(self, user_id: UserId) -> int:
        counter = await self._repository.search(user_id)
        if not counter:
            return 0

        return counter.total.value
