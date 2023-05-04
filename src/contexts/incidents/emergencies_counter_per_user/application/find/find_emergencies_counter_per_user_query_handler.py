from typing import Type

from contexts.incidents.emergencies_counter_per_user.application.find.emergencies_counter_per_user_finder import (
    EmergenciesCounterPerUserFinder,
)
from contexts.incidents.emergencies_counter_per_user.application.find.find_emergencies_counter_per_user_query import (
    FindEmergenciesCounterPerUserQuery,
)
from contexts.incidents.emergencies_counter_per_user.application.find.find_emergencies_counter_per_user_response import (
    FindEmergenciesCounterPerUserResponse,
)
from contexts.incidents.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.query import Query, QueryHandler


class FindEmergenciesCounterPerUserQueryHandler(QueryHandler):
    def __init__(self, finder: EmergenciesCounterPerUserFinder):
        self._finder = finder

    def subscribed_to(self) -> Type[Query]:
        return FindEmergenciesCounterPerUserQuery

    async def __call__(
        self, query: FindEmergenciesCounterPerUserQuery
    ) -> FindEmergenciesCounterPerUserResponse:
        user_id = UserId(query.user_id)
        count = await self._finder(user_id)

        return FindEmergenciesCounterPerUserResponse(total=count)
