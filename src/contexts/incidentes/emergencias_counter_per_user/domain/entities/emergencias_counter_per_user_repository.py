from abc import ABC, abstractmethod

from contexts.incidentes.emergencias_counter_per_user.domain.entities.emergencias_counter_per_user import (
    EmergenciasCounterPerUser,
)
from contexts.incidentes.shared.domain.value_objects import UserId


class EmergenciasCounterPerUserRepository(ABC):
    @abstractmethod
    async def search(self, user_id: UserId) -> EmergenciasCounterPerUser | None:
        pass

    @abstractmethod
    async def save(self, counter: EmergenciasCounterPerUser) -> None:
        pass
