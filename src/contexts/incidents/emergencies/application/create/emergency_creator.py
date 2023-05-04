from contexts.incidents.emergencies.domain.entities import (
    Emergency,
    EmergencyRepository,
)
from contexts.incidents.emergencies.domain.value_objects import (
    EmergencyAbscissa,
    EmergencyCode,
)
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.event import EventBus


class EmergencyCreator:
    def __init__(self, repository: EmergencyRepository, bus: EventBus):
        self._repository = repository
        self._bus = bus

    async def create(
        self,
        _id: EmergencyId,
        abscissa: EmergencyAbscissa,
        user_id: UserId,
    ) -> None:
        """
        FIXME: handle potential race conditions on code generation
        """
        last_code = await self._repository.last_code()
        next_code = EmergencyCode.generate(last_code)

        emergency = Emergency.create(
            _id=_id, code=next_code, abscissa=abscissa, user_id=user_id
        )

        await self._repository.save(emergency)

        await self._bus.publish(*emergency.pull_domain_events())
