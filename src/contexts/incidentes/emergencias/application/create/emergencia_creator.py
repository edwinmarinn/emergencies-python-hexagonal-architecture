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

    async def create(
        self,
        _id: EmergenciaId,
        abscisa: EmergenciaAbscisa,
        usuario_id: UsuarioId,
    ) -> None:
        """
        FIXME: handle potential race conditions on code generation
        """
        last_code = await self._repository.last_code()
        next_code = EmergenciaCode.generate(last_code)

        emergencia = Emergencia.create(
            _id=_id, code=next_code, abscisa=abscisa, usuario_id=usuario_id
        )

        self._repository.save(emergencia)

        self._bus.publish(*emergencia.pullDomainEvents())
