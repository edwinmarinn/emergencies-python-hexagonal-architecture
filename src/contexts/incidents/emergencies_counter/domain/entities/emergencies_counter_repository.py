from abc import ABC, abstractmethod

from contexts.incidents.emergencies_counter.domain.entities.emergencies_counter import (
    EmergenciesCounter,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId


class EmergenciesCounterRepository(ABC):
    @abstractmethod
    async def increment(
        self, counter: EmergenciesCounter, emergency_id: EmergencyId
    ) -> EmergenciesCounter:
        pass

    @abstractmethod
    async def has_incremented(self, emergency_id: EmergencyId) -> bool:
        pass

    @abstractmethod
    async def search(self) -> EmergenciesCounter | None:
        pass
