from typing import Type

from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.shared.domain.bus.query import Query, QueryHandler

from .emergencia_finder import EmergenciaFinder
from .emergencia_response import EmergenciaResponse
from .emergencia_response_converter import EmergenciaResponseConverter
from .find_emergencia_query import FindEmergenciaQuery


class FindEmergenciaQueryHandler(QueryHandler):
    _converter = EmergenciaResponseConverter()

    def __init__(self, finder: EmergenciaFinder):
        self._finder = finder

    def subscribed_to(self) -> Type[Query]:
        return FindEmergenciaQuery

    async def __call__(self, query: FindEmergenciaQuery) -> EmergenciaResponse:
        _id = EmergenciaId(query.id)
        emergencia = await self._finder(_id)
        emergencia_response = self._converter(emergencia)
        return emergencia_response
