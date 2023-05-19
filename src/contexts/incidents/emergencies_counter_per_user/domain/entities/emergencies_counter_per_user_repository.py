from abc import ABC, abstractmethod

from contexts.incidents.emergencies_counter_per_user.domain.entities.emergencies_counter_per_user import (
    EmergenciesCounterPerUser,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId


class EmergenciesCounterPerUserRepository(ABC):
    @abstractmethod
    async def has_incremented(self, emergency_id: EmergencyId) -> bool:
        pass

    @abstractmethod
    async def increment(
        self, user_id: UserId, emergency_id: EmergencyId
    ) -> EmergenciesCounterPerUser:
        pass

    @abstractmethod
    async def search(self, user_id: UserId) -> EmergenciesCounterPerUser | None:
        pass
