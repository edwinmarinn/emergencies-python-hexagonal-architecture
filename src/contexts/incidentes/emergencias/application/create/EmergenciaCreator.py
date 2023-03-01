from contexts.incidentes.emergencias.domain.entities import (
    Emergencia,
    EmergenciaRepository,
)
from contexts.incidentes.emergencias.domain.value_objects import (
    EmergenciaAbscisa,
    EmergenciaCode,
    EmergenciaId,
)
from contexts.incidentes.shared.domain.value_objects import UsuarioId
from contexts.shared.domain.bus.event import EventBus


class EmergenciaCreator:
    def __init__(self, repository: EmergenciaRepository, bus: EventBus):
        self._repository = repository
        self._bus = bus

    def create(
        self,
        _id: EmergenciaId,
        code: EmergenciaCode,
        abscisa: EmergenciaAbscisa,
        usuario_id: UsuarioId,
    ) -> None:
        emergencia = Emergencia.create(
            _id=_id, code=code, abscisa=abscisa, usuario_id=usuario_id
        )

        self._repository.save(emergencia)

        self._bus.publish(*emergencia.pullDomainEvents())
