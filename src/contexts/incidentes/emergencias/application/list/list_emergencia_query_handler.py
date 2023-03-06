from typing import List

from contexts.shared.domain.bus.query import QueryHandler
from contexts.shared.domain.criteria import Order, OrderBy, OrderType

from .emergencia_filters import EmergenciaFilters
from .emergencia_lister import EmergenciaLister
from .emergencia_response import EmergenciaResponse
from .emergencia_response_converter import EmergenciaResponseConverter
from .list_emergencia_query import ListEmergenciaQuery


class ListEmergenciaQueryHandler(QueryHandler):
    _converter = EmergenciaResponseConverter()

    def __init__(self, lister: EmergenciaLister):
        self._lister = lister

    async def __call__(self, query: ListEmergenciaQuery) -> List[EmergenciaResponse]:
        filters = EmergenciaFilters.from_json_str(query.filters)
        order = Order(OrderBy(query.order_by), OrderType(query.order_type))

        emergencias = await self._lister(
            filters=filters, order=order, offset=query.offset, limit=query.limit
        )
        emergencias_response = self._converter(emergencias)
        return emergencias_response
