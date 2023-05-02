from abc import ABC, abstractmethod

from contexts.incidentes.emergencias_counter.domain.entities.emergencias_counter import (
    EmergenciasCounter,
)


class EmergenciasCounterRepository(ABC):
    @abstractmethod
    async def search(self) -> EmergenciasCounter | None:
        pass

    @abstractmethod
    async def save(self, counter: EmergenciasCounter) -> None:
        pass
