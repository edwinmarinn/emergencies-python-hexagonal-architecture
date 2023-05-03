from contexts.incidentes.emergencias.domain.entities import Emergencia, Emergencias

from .emergencias_response import EmergenciaResponse, EmergenciasResponse


class EmergenciasResponseConverter:
    @staticmethod
    def converter(emergencia: Emergencia) -> EmergenciaResponse:
        return EmergenciaResponse(
            id=emergencia.id.value,
            code=emergencia.code.value,
            abscisa=emergencia.abscisa.value,
            user_id=emergencia.user_id.value,
        )

    def __call__(self, emergencias: Emergencias) -> EmergenciasResponse:
        return EmergenciasResponse(list(map(self.converter, emergencias)))
