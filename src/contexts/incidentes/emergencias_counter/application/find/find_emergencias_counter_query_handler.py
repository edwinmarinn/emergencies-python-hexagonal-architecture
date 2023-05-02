from typing import Type

from contexts.incidentes.emergencias_counter.application.find.emergencias_counter_finder import (
    EmergenciasCounterFinder,
)
from contexts.incidentes.emergencias_counter.application.find.find_emergencias_counter_query import (
    FindEmergenciasCounterQuery,
)
from contexts.incidentes.emergencias_counter.application.find.find_emergencias_counter_response import (
    FindEmergenciasCounterResponse,
)
from contexts.shared.domain.bus.query import Query, QueryHandler


class FindEmergenciasCounterQueryHandler(QueryHandler):
    def __init__(self, finder: EmergenciasCounterFinder):
        self._finder = finder

    def subscribed_to(self) -> Type[Query]:
        return FindEmergenciasCounterQuery

    async def __call__(
        self, query: FindEmergenciasCounterQuery
    ) -> FindEmergenciasCounterResponse:
        count = await self._finder()
        return FindEmergenciasCounterResponse(total=count)
