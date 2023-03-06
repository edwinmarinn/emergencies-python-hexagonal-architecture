from abc import ABC, abstractmethod

from contexts.incidentes.emergencias.domain.entities import Emergencia
from contexts.incidentes.emergencias.domain.entities.emergencias import Emergencias
from contexts.incidentes.emergencias.domain.value_objects import EmergenciaId
from contexts.shared.domain.criteria import Criteria


class EmergenciaRepository(ABC):
    @staticmethod
    @abstractmethod
    def save(emergencia: Emergencia) -> None:
        pass

    @staticmethod
    @abstractmethod
    async def search(emergencia_id: EmergenciaId) -> Emergencia | None:
        pass

    @staticmethod
    @abstractmethod
    async def search_by_criteria(criteria: Criteria) -> Emergencias:
        pass
