from abc import ABC, abstractmethod

from contexts.incidents.emergencies_counter.domain.entities.emergencies_counter import (
    EmergenciesCounter,
)


class EmergenciesCounterRepository(ABC):
    @abstractmethod
    async def save(self, counter: EmergenciesCounter) -> None:
        pass

    @abstractmethod
    async def search(self) -> EmergenciesCounter | None:
        pass
