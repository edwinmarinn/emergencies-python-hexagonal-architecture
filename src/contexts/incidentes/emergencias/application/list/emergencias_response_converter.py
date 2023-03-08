from typing import List

from contexts.incidentes.emergencias.domain.entities import Emergencia, Emergencias

from .emergencia_response import EmergenciaResponse


class EmergenciasResponseConverter:
    @staticmethod
    def converter(emergencia: Emergencia) -> EmergenciaResponse:
        return EmergenciaResponse(
            id=emergencia.id.value,
            code=emergencia.code.value,
            abscisa=emergencia.abscisa.value,
            usuario_id=emergencia.usuario_id.value,
        )

    def __call__(self, emergencias: Emergencias) -> List[EmergenciaResponse]:
        return list(map(self.converter, emergencias))
