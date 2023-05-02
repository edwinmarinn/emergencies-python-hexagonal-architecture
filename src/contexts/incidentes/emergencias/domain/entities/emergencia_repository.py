from abc import ABC, abstractmethod

from contexts.incidentes.emergencias.domain.entities import Emergencia
from contexts.incidentes.emergencias.domain.entities.emergencias import Emergencias
from contexts.incidentes.emergencias.domain.value_objects import EmergenciaCode
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.shared.domain.criteria import Criteria


class EmergenciaRepository(ABC):
    @abstractmethod
    async def save(self, emergencia: Emergencia) -> None:
        pass

    @abstractmethod
    async def search(self, emergencia_id: EmergenciaId) -> Emergencia | None:
        pass

    @abstractmethod
    async def search_by_criteria(self, criteria: Criteria) -> Emergencias:
        pass

    @abstractmethod
    async def last_code(self) -> EmergenciaCode | None:
        pass
