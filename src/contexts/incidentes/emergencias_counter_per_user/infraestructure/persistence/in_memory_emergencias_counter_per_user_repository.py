from typing import Dict

from contexts.incidentes.emergencias_counter_per_user.domain.entities.emergencias_counter_per_user import (
    EmergenciasCounterPerUser,
)
from contexts.incidentes.emergencias_counter_per_user.domain.entities.emergencias_counter_per_user_repository import (
    EmergenciasCounterPerUserRepository,
)
from contexts.incidentes.shared.domain.value_objects import UserId


class InMemoryEmergenciasCounterPerUserRepository(EmergenciasCounterPerUserRepository):
    def __init__(self):
        self._data: Dict[UserId, EmergenciasCounterPerUser] = {}

    async def search(self, user_id: UserId) -> EmergenciasCounterPerUser | None:
        return self._data.get(user_id)

    async def save(self, counter: EmergenciasCounterPerUser) -> None:
        self._data[counter.user_id] = counter
