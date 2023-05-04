from typing import Type

from contexts.incidents.emergencies_counter.application.find.emergencies_counter_finder import (
    EmergenciesCounterFinder,
)
from contexts.incidents.emergencies_counter.application.find.find_emergencies_counter_query import (
    FindEmergenciesCounterQuery,
)
from contexts.incidents.emergencies_counter.application.find.find_emergencies_counter_response import (
    FindEmergenciesCounterResponse,
)
from contexts.shared.domain.bus.query import Query, QueryHandler


class FindEmergenciesCounterQueryHandler(QueryHandler):
    def __init__(self, finder: EmergenciesCounterFinder):
        self._finder = finder

    def subscribed_to(self) -> Type[Query]:
        return FindEmergenciesCounterQuery

    async def __call__(
        self, query: FindEmergenciesCounterQuery
    ) -> FindEmergenciesCounterResponse:
        count = await self._finder()
        return FindEmergenciesCounterResponse(total=count)
