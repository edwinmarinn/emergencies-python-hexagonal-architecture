from typing import Dict

from contexts.incidentes.emergencias.domain.entities import (
    Emergencia,
    EmergenciaRepository,
    Emergencias,
)
from contexts.incidentes.emergencias.domain.value_objects import (
    EmergenciaCode,
    EmergenciaId,
)
from contexts.shared.domain.criteria import Criteria


class InMemoryEmergenciaRepository(EmergenciaRepository):
    def __init__(self):
        self._data: Dict[EmergenciaId, Emergencia] = {}

    def save(self, emergencia: Emergencia) -> None:
        self._data[emergencia.id] = emergencia

    async def search(self, emergencia_id: EmergenciaId) -> Emergencia | None:
        return self._data.get(emergencia_id)

    async def search_by_criteria(self, criteria: Criteria) -> Emergencias:
        # Todo: apply criteria search pattern
        return Emergencias(list(self._data.values()))

    async def last_code(self) -> EmergenciaCode | None:
        return None
