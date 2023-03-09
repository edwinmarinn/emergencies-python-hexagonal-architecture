from typing import List

from contexts.shared.domain.bus.query import QueryHandler
from contexts.shared.domain.criteria import Order, OrderBy, OrderType

from .emergencia_response import EmergenciaResponse
from .emergencias_filters import EmergenciasFilters
from .emergencias_lister import EmergenciasLister
from .emergencias_response_converter import EmergenciasResponseConverter
from .list_emergencias_query import ListEmergenciasQuery


class ListEmergenciasQueryHandler(QueryHandler):
    _converter = EmergenciasResponseConverter()

    def __init__(self, lister: EmergenciasLister):
        self._lister = lister

    async def __call__(self, query: ListEmergenciasQuery) -> List[EmergenciaResponse]:  # type: ignore[override]
        filters = EmergenciasFilters.from_json_str(query.filters)
        order = Order(OrderBy(query.order_by), OrderType(query.order_type))

        emergencias = await self._lister(
            filters=filters, order=order, offset=query.offset, limit=query.limit
        )
        emergencias_response = self._converter(emergencias)
        return emergencias_response
