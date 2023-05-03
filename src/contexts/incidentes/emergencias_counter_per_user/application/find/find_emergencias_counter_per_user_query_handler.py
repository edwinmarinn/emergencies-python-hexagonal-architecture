from typing import Type

from contexts.incidentes.emergencias_counter_per_user.application.find.emergencias_counter_per_user_finder import (
    EmergenciasCounterPerUserFinder,
)
from contexts.incidentes.emergencias_counter_per_user.application.find.find_emergencias_counter_per_user_query import (
    FindEmergenciasCounterPerUserQuery,
)
from contexts.incidentes.emergencias_counter_per_user.application.find.find_emergencias_counter_per_user_response import (
    FindEmergenciasCounterPerUserResponse,
)
from contexts.incidentes.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.query import Query, QueryHandler


class FindEmergenciasCounterPerUserQueryHandler(QueryHandler):
    def __init__(self, finder: EmergenciasCounterPerUserFinder):
        self._finder = finder

    def subscribed_to(self) -> Type[Query]:
        return FindEmergenciasCounterPerUserQuery

    async def __call__(
        self, query: FindEmergenciasCounterPerUserQuery
    ) -> FindEmergenciasCounterPerUserResponse:
        user_id = UserId(query.user_id)
        count = await self._finder(user_id)

        return FindEmergenciasCounterPerUserResponse(total=count)
