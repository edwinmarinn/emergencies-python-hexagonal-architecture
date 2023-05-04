from abc import ABC, abstractmethod

from contexts.incidents.emergencies_counter_per_user.domain.entities.emergencies_counter_per_user import (
    EmergenciesCounterPerUser,
)
from contexts.incidents.shared.domain.value_objects import UserId


class EmergenciesCounterPerUserRepository(ABC):
    @abstractmethod
    async def search(self, user_id: UserId) -> EmergenciesCounterPerUser | None:
        pass

    @abstractmethod
    async def save(self, counter: EmergenciesCounterPerUser) -> None:
        pass
