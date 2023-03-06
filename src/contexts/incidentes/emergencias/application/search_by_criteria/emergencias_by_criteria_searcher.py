from contexts.incidentes.emergencias.domain.entities import EmergenciaRepository
from contexts.incidentes.emergencias.domain.entities.emergencias import Emergencias
from contexts.shared.domain.criteria import Criteria, Filters, Order


class EmergenciasByCriteriaSearcher:
    def __init__(self, repository: EmergenciaRepository):
        self._repository = repository

    async def run(
        self, filters: Filters, order: Order, offset: int, limit: int
    ) -> Emergencias:
        criteria = Criteria(filters=filters, order=order, offset=offset, limit=limit)

        emergencias = await self._repository.search_by_criteria(criteria)

        return emergencias
