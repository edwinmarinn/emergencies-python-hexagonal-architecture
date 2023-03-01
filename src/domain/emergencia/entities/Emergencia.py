from dataclasses import dataclass

from domain.emergencia.entities.EmergenciaCreatedDomainEvent import (
    EmergenciaCreatedDomainEvent,
)
from domain.emergencia.value_objects import EmergenciaId
from domain.emergencia.value_objects import EmergenciaCode
from domain.emergencia.value_objects import EmergenciaAbscisa
from domain.shared.aggregate import AggregateRoot
from domain.shared.value_objects import UsuarioId


@dataclass
class Emergencia(AggregateRoot):
    id: EmergenciaId
    code: EmergenciaCode
    abscisa: EmergenciaAbscisa
    usuario_id: UsuarioId

    # def __init__(
    #     self,
    #     _id: EmergenciaId,
    #     code: EmergenciaCode,
    #     abscisa: EmergenciaAbscisa,
    #     usuario_id: UsuarioId,
    # ):
    #     super().__init__()
    #     self.id = _id
    #     self.code = code
    #     self.abscisa = abscisa
    #     self.usuario_id = usuario_id

    @classmethod
    def create(
        cls,
        _id: EmergenciaId,
        code: EmergenciaCode,
        abscisa: EmergenciaAbscisa,
        usuario_id: UsuarioId,
    ):
        emergencia = cls(id=_id, code=code, abscisa=abscisa, usuario_id=usuario_id)

        emergencia.record(
            EmergenciaCreatedDomainEvent(
                _id=_id.value,
                data=dict(
                    code=code.value, abscisa=abscisa.value, usuario_id=usuario_id.value
                ),
            )
        )

        return emergencia
