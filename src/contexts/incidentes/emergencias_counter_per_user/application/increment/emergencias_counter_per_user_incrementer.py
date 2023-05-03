from contexts.incidentes.emergencias_counter_per_user.domain.entities import (
    EmergenciasCounterPerUser,
    EmergenciasCounterPerUserRepository,
)
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.incidentes.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.event import EventBus


class EmergenciasCounterPerUserIncrementer:
    def __init__(self, repository: EmergenciasCounterPerUserRepository, bus: EventBus):
        self._repository = repository
        self._bus = bus

    async def __call__(self, user_id: UserId, emergencia_id: EmergenciaId) -> None:
        counter = (await self._repository.search(user_id)) or self.initialize_counter(
            user_id
        )

        if not counter.has_incremented(emergencia_id):
            counter.increment(emergencia_id)

            await self._repository.save(counter)
            await self._bus.publish(*counter.pull_domain_events())

    @staticmethod
    def initialize_counter(user_id: UserId) -> EmergenciasCounterPerUser:
        return EmergenciasCounterPerUser.initialize(user_id)
