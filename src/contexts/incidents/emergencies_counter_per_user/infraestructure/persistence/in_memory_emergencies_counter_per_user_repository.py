from typing import Dict

from contexts.incidents.emergencies_counter_per_user.domain.entities.emergencies_counter_per_user import (
    EmergenciesCounterPerUser,
)
from contexts.incidents.emergencies_counter_per_user.domain.entities.emergencies_counter_per_user_repository import (
    EmergenciesCounterPerUserRepository,
)
from contexts.incidents.shared.domain.value_objects import UserId


class InMemoryEmergenciesCounterPerUserRepository(EmergenciesCounterPerUserRepository):
    def __init__(self):
        self._data: Dict[UserId, EmergenciesCounterPerUser] = {}

    async def search(self, user_id: UserId) -> EmergenciesCounterPerUser | None:
        return self._data.get(user_id)

    async def save(self, counter: EmergenciesCounterPerUser) -> None:
        self._data[counter.user_id] = counter
