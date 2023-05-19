from contexts.incidents.emergencies.domain.entities import (
    Emergencies,
    Emergency,
    EmergencyRepository,
)
from contexts.incidents.emergencies.domain.value_objects import EmergencyCode
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.shared.domain.criteria import Criteria


class InMemoryEmergencyRepository(EmergencyRepository):
    def __init__(self):
        self._data: dict[EmergencyId, Emergency] = {}

    async def save(self, emergency: Emergency) -> None:
        self._data[emergency.id] = emergency

    async def search(self, emergency_id: EmergencyId) -> Emergency | None:
        return self._data.get(emergency_id)

    async def search_by_criteria(self, criteria: Criteria) -> Emergencies:
        # Todo: apply criteria search pattern
        return Emergencies(list(self._data.values()))

    async def last_code(self) -> EmergencyCode | None:
        return None
