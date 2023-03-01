from dataclasses import dataclass

from .EmergenciaCreatedDomainEvent import EmergenciaCreatedDomainEvent
from contexts.incidentes.emergencias.domain.value_objects import (
    EmergenciaAbscisa,
    EmergenciaCode,
    EmergenciaId,
)
from contexts.incidentes.shared.domain.value_objects import UsuarioId
from contexts.shared.domain.aggregate import AggregateRoot


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
    ):
        emergencia = cls(_id=_id, code=code, abscisa=abscisa, usuario_id=usuario_id)

        emergencia.record(
            EmergenciaCreatedDomainEvent(
                _id=_id.value,
                data=dict(
                    code=code.value, abscisa=abscisa.value, usuario_id=usuario_id.value
                ),
            )
        )

        return emergencia
