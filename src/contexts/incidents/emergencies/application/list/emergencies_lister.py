from contexts.incidents.emergencies.domain.entities import (
    Emergencies,
    EmergencyRepository,
)
from contexts.shared.domain.criteria import Criteria, Order

from .emergencies_filters import EmergenciesFilters


class EmergenciesLister:
    def __init__(self, repository: EmergencyRepository):
        self._repository = repository

    async def __call__(
        self, filters: EmergenciesFilters, order: Order, offset: int, limit: int
    ) -> Emergencies:
        criteria = Criteria(filters=filters, order=order, offset=offset, limit=limit)

        emergencies = await self._repository.search_by_criteria(criteria)

        return emergencies
