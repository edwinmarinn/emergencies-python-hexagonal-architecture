"""
Este servicio de dominio es utilizado en varios servicios de la capa de aplicación,
por eso se crea aca y no en la capa de aplicación
"""
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId

from .emergency import Emergency
from .emergency_not_found import EmergencyNotFound
from .emergency_repository import EmergencyRepository


class EmergencyFinder:
    def __init__(self, repository: EmergencyRepository):
        self._repository = repository

    async def __call__(self, _id: EmergencyId) -> Emergency:
        emergency = await self._repository.search(_id)
        emergency = self._ensure_emergency_exists(_id, emergency)

        return emergency

    @staticmethod
    def _ensure_emergency_exists(
        _id: EmergencyId, emergency: Emergency | None = None
    ) -> Emergency:
        if emergency is None:
            raise EmergencyNotFound(_id)
        return emergency
