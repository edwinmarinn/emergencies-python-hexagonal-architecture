from contexts.incidents.emergencies.domain.entities import EmergencyRepository
from contexts.incidents.emergencies.domain.entities.emergencies import Emergencies
from contexts.shared.domain.criteria import Criteria, Filters, Order


class EmergenciesByCriteriaSearcher:
    def __init__(self, repository: EmergencyRepository):
        self._repository = repository

    async def run(
        self, filters: Filters, order: Order, offset: int, limit: int
    ) -> Emergencies:
        criteria = Criteria(filters=filters, order=order, offset=offset, limit=limit)

        emergencies = await self._repository.search_by_criteria(criteria)

        return emergencies
