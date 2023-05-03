from typing_extensions import Self

from contexts.incidentes.emergencias.domain.value_objects import (
    EmergenciaAbscisa,
    EmergenciaCode,
)
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.incidentes.shared.domain.value_objects import UserId
from contexts.shared.domain.aggregate import AggregateRoot

from .emergencia_created_domain_event import EmergenciaCreatedDomainEvent


class Emergencia(AggregateRoot):
    def __init__(
        self,
        _id: EmergenciaId,
        code: EmergenciaCode,
        abscisa: EmergenciaAbscisa,
        user_id: UserId,
    ):
        super().__init__()
        self.id = _id
        self.code = code
        self.abscisa = abscisa
        self.user_id = user_id

    @classmethod
    def create(
        cls,
        _id: EmergenciaId,
        code: EmergenciaCode,
        abscisa: EmergenciaAbscisa,
        user_id: UserId,
    ) -> Self:
        emergencia = cls(_id=_id, code=code, abscisa=abscisa, user_id=user_id)

        emergencia.record(
            EmergenciaCreatedDomainEvent(
                aggregate_id=_id.value,
                data=dict(
                    code=code.value, abscisa=abscisa.value, user_id=user_id.value
                ),
            )
        )

        return emergencia
