from contexts.incidents.emergencies_counter_per_user.domain.entities.emergencies_counter_per_user import (
    EmergenciesCounterPerUser,
)
from contexts.incidents.emergencies_counter_per_user.domain.entities.emergencies_counter_per_user_repository import (
    EmergenciesCounterPerUserRepository,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId


class InMemoryEmergenciesCounterPerUserRepository(EmergenciesCounterPerUserRepository):
    def __init__(self):
        self._data: dict[UserId, EmergenciesCounterPerUser] = {}
        self._emergencies_id: set[EmergencyId] = set()

    async def has_incremented(self, emergency_id: EmergencyId) -> bool:
        return emergency_id in self._emergencies_id

    async def increment(
        self, user_id: UserId, emergency_id: EmergencyId
    ) -> EmergenciesCounterPerUser:
        self._emergencies_id.add(emergency_id)

        if user_id not in self._data:
            self._data[user_id] = EmergenciesCounterPerUser.initialize(user_id=user_id)

        counter = self._data[user_id]
        self._data[user_id] = EmergenciesCounterPerUser(
            user_id=counter.user_id, total=counter.total.increment()
        )
        return self._data[user_id]

    async def search(self, user_id: UserId) -> EmergenciesCounterPerUser | None:
        return self._data.get(user_id, None)
