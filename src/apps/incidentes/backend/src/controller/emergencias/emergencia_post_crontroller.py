from typing import Dict

from contexts.incidentes.emergencias.application.create import CreateEmergenciaCommand
from contexts.shared.infrastructure.api.controller.api_controller import ApiController
from contexts.shared.infrastructure.api.response import ApiHttpCreatedResponse


class EmergenciaPostController(ApiController):
    def exceptions(self) -> Dict[str, int]:
        return {}

    def __call__(self, request):
        command = CreateEmergenciaCommand(
            id=request.get("id"),
            abscisa=request.get("abscisa"),
            usuario_id=request.get("usuario_id"),
        )

        self.dispatch(command)

        return ApiHttpCreatedResponse()
