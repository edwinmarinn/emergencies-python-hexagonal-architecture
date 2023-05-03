from contexts.incidentes.emergencias.domain.entities import (
    Emergencia,
    EmergenciaRepository,
)
from contexts.incidentes.emergencias.domain.value_objects import (
    EmergenciaAbscisa,
    EmergenciaCode,
)
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.incidentes.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.event import EventBus


class EmergenciaCreator:
    def __init__(self, repository: EmergenciaRepository, bus: EventBus):
        self._repository = repository
        self._bus = bus

    async def create(
        self,
        _id: EmergenciaId,
        abscisa: EmergenciaAbscisa,
        user_id: UserId,
    ) -> None:
        """
        FIXME: handle potential race conditions on code generation
        """
        last_code = await self._repository.last_code()
        next_code = EmergenciaCode.generate(last_code)

        emergencia = Emergencia.create(
            _id=_id, code=next_code, abscisa=abscisa, user_id=user_id
        )

        await self._repository.save(emergencia)

        await self._bus.publish(*emergencia.pull_domain_events())
