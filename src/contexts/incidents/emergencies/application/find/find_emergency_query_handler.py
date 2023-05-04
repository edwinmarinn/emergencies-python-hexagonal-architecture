from typing import Type

from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.shared.domain.bus.query import Query, QueryHandler

from .emergency_finder import EmergencyFinder
from .emergency_response import EmergencyResponse
from .emergency_response_converter import EmergencyResponseConverter
from .find_emergency_query import FindEmergencyQuery


class FindEmergencyQueryHandler(QueryHandler):
    _converter = EmergencyResponseConverter()

    def __init__(self, finder: EmergencyFinder):
        self._finder = finder

    def subscribed_to(self) -> Type[Query]:
        return FindEmergencyQuery

    async def __call__(self, query: FindEmergencyQuery) -> EmergencyResponse:
        _id = EmergencyId(query.id)
        emergency = await self._finder(_id)
        emergency_response = self._converter(emergency)
        return emergency_response
