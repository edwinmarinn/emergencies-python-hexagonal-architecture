from http import HTTPStatus
from typing import Dict

from contexts.incidentes.emergencias.application.find import FindEmergenciaQuery
from contexts.incidentes.emergencias.domain.entities import EmergenciaNotFound
from contexts.shared.infrastructure.api.controller.api_controller import ApiController


class EmergenciaGetController(ApiController):
    def exceptions(self) -> Dict[str, int]:
        return {EmergenciaNotFound.__name__: HTTPStatus.NOT_FOUND}

    def __call__(self, _id: str):
        return self.ask(FindEmergenciaQuery(_id))
