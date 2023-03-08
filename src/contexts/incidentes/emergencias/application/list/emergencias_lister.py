from contexts.incidentes.emergencias.domain.entities import (
    EmergenciaRepository,
    Emergencias,
)
from contexts.shared.domain.criteria import Criteria, Order

from .emergencias_filters import EmergenciasFilters


class EmergenciasLister:
    def __init__(self, repository: EmergenciaRepository):
        self._repository = repository

    async def __call__(
        self, filters: EmergenciasFilters, order: Order, offset: int, limit: int
    ) -> Emergencias:
        criteria = Criteria(filters=filters, order=order, offset=offset, limit=limit)

        emergencias = await self._repository.search_by_criteria(criteria)

        return emergencias
