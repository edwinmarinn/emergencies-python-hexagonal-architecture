from contexts.incidentes.emergencias.application.find.emergencia_response import (
    EmergenciaResponse,
)
from contexts.incidentes.emergencias.domain.entities import Emergencia


class EmergenciaResponseConverter:
    def __call__(self, emergencia: Emergencia):
        return EmergenciaResponse(
            id=emergencia.id.value,
            code=emergencia.code.value,
            abscisa=emergencia.abscisa.value,
            usuario_id=emergencia.usuario_id.value,
        )
