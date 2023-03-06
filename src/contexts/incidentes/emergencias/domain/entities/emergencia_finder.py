"""
Este servicio de dominio es utilizado en varios servicios de la capa de aplicación,
por eso se crea aca y no en la capa de aplicación
"""
from contexts.incidentes.emergencias.domain.value_objects import EmergenciaId

from .emergencia import Emergencia
from .emergencia_not_found import EmergenciaNotFound
from .emergencia_repository import EmergenciaRepository


class EmergenciaFinder:
    def __init__(self, repository: EmergenciaRepository):
        self._repository = repository

    async def __call__(self, _id: EmergenciaId) -> Emergencia | None:
        emergencia = await self._repository.search(_id)
        self._ensure_emergencia_exists(_id, emergencia)

        return emergencia

    @staticmethod
    def _ensure_emergencia_exists(
        _id: EmergenciaId, emergencia: Emergencia = None
    ) -> None:
        if emergencia is None:
            raise EmergenciaNotFound
