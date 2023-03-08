from typing import Dict

from contexts.incidentes.emergencias.application.list import ListEmergenciasQuery
from contexts.shared.infrastructure.api.controller.api_controller import ApiController


class EmergenciaListController(ApiController):
    def exceptions(self) -> Dict[str, int]:
        return {}

    def __call__(
        self, filters: str, order_by: str, order_type: str, offset: int, limit: int
    ):
        return self.ask(
            ListEmergenciasQuery(
                filters=filters,
                order_by=order_by,
                order_type=order_type,
                offset=offset,
                limit=limit,
            )
        )
