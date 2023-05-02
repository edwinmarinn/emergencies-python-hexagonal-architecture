from contexts.incidentes.emergencias_counter.domain.entities.emergencias_counter import (
    EmergenciasCounter,
)
from contexts.incidentes.emergencias_counter.domain.entities.emergencias_counter_repository import (
    EmergenciasCounterRepository,
)
from contexts.incidentes.emergencias_counter.domain.value_objects.emergencias_counter_id import (
    EmergenciasCounterId,
)
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.shared.domain.bus.event import EventBus


class EmergenciasCounterIncrementer:
    def __init__(self, repository: EmergenciasCounterRepository, bus: EventBus):
        self._repository = repository
        self._bus = bus

    async def __call__(self, emergencia_id: EmergenciaId):
        counter = (await self._repository.search()) or self.initialize_counter()

        if not counter.has_incremented(emergencia_id):
            counter.increment(emergencia_id)

            await self._repository.save(counter)
            await self._bus.publish(*counter.pull_domain_events())

    @staticmethod
    def initialize_counter() -> EmergenciasCounter:
        return EmergenciasCounter.initialize(EmergenciasCounterId.random())
