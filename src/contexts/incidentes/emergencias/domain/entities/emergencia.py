from typing_extensions import Self

from contexts.incidentes.emergencias.domain.value_objects import (
    EmergenciaAbscisa,
    EmergenciaCode,
)
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.incidentes.shared.domain.value_objects import UsuarioId
from contexts.shared.domain.aggregate import AggregateRoot

from .emergencia_created_domain_event import EmergenciaCreatedDomainEvent


class Emergencia(AggregateRoot):
    def __init__(
        self,
        _id: EmergenciaId,
        code: EmergenciaCode,
        abscisa: EmergenciaAbscisa,
        usuario_id: UsuarioId,
    ):
        super().__init__()
        self.id = _id
        self.code = code
        self.abscisa = abscisa
        self.usuario_id = usuario_id

    @classmethod
    def create(
        cls,
        _id: EmergenciaId,
        code: EmergenciaCode,
        abscisa: EmergenciaAbscisa,
        usuario_id: UsuarioId,
    ) -> Self:
        emergencia = cls(_id=_id, code=code, abscisa=abscisa, usuario_id=usuario_id)

        emergencia.record(
            EmergenciaCreatedDomainEvent(
                aggregate_id=_id.value,
                data=dict(
                    code=code.value, abscisa=abscisa.value, usuario_id=usuario_id.value
                ),
            )
        )

        return emergencia
