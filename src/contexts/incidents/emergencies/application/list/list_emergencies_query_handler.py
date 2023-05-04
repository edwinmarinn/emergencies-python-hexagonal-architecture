from typing import List, Type

from contexts.shared.domain.bus.query import Query, QueryHandler
from contexts.shared.domain.criteria import Order, OrderBy, OrderType

from .emergencies_filters import EmergenciesFilters
from .emergencies_lister import EmergenciesLister
from .emergencies_response import EmergenciesResponse, EmergencyResponse
from .emergencies_response_converter import EmergenciesResponseConverter
from .list_emergencies_query import ListEmergenciesQuery


class ListEmergenciesQueryHandler(QueryHandler):
    _converter = EmergenciesResponseConverter()

    def __init__(self, lister: EmergenciesLister):
        self._lister = lister

    def subscribed_to(self) -> Type[Query]:
        return ListEmergenciesQuery

    async def __call__(self, query: ListEmergenciesQuery) -> EmergenciesResponse:
        filters = EmergenciesFilters.from_json_str(query.filters)
        order = Order(OrderBy(query.order_by), OrderType(query.order_type))

        emergencies = await self._lister(
            filters=filters, order=order, offset=query.offset, limit=query.limit
        )
        emergencies_response = self._converter(emergencies)
        return emergencies_response
