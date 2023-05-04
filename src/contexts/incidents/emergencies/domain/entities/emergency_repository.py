from abc import ABC, abstractmethod

from contexts.incidents.emergencies.domain.entities import Emergency
from contexts.incidents.emergencies.domain.entities.emergencies import Emergencies
from contexts.incidents.emergencies.domain.value_objects import EmergencyCode
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.shared.domain.criteria import Criteria


class EmergencyRepository(ABC):
    @abstractmethod
    async def save(self, emergency: Emergency) -> None:
        pass

    @abstractmethod
    async def search(self, emergency_id: EmergencyId) -> Emergency | None:
        pass

    @abstractmethod
    async def search_by_criteria(self, criteria: Criteria) -> Emergencies:
        pass

    @abstractmethod
    async def last_code(self) -> EmergencyCode | None:
        pass
