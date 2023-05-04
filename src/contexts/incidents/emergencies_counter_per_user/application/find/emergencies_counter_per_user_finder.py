from contexts.incidents.emergencies_counter_per_user.domain.entities import (
    EmergenciesCounterPerUserRepository,
)
from contexts.incidents.shared.domain.value_objects import UserId


class EmergenciesCounterPerUserFinder:
    def __init__(self, repository: EmergenciesCounterPerUserRepository):
        self._repository = repository

    async def __call__(self, user_id: UserId) -> int:
        counter = await self._repository.search(user_id)
        if not counter:
            return 0

        return counter.total.value
