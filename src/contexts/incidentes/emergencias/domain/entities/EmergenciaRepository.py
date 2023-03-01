from abc import ABC, abstractmethod
from typing import Optional

from contexts.incidentes.emergencias.domain.entities import Emergencia
from contexts.incidentes.emergencias.domain.value_objects import EmergenciaId


class EmergenciaRepository(ABC):
    @staticmethod
    @abstractmethod
    def save(emergencia: Emergencia) -> None:
        pass

    @staticmethod
    @abstractmethod
    def search(emergencia_id: EmergenciaId) -> Optional[Emergencia]:
        pass

    # @staticmethod
    # @abstractmethod
    # def searchByCriteria(criteria: Criteria): Emergencias;
    #     pass
