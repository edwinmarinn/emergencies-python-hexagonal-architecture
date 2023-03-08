from contexts.incidentes.emergencias.domain.entities import Emergencia
from contexts.incidentes.emergencias.domain.entities import (
    EmergenciaFinder as EmergenciaFinderDomain,
)
from contexts.incidentes.emergencias.domain.entities import EmergenciaRepository
from contexts.incidentes.emergencias.domain.value_objects import EmergenciaId


class EmergenciaFinder:
    def __init__(self, repository: EmergenciaRepository):
        self._finder = EmergenciaFinderDomain(repository)

    async def __call__(self, _id: EmergenciaId) -> Emergencia:
        emergencia = await self._finder(_id)
        return emergencia
