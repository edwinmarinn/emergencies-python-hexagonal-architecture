from contexts.incidents.emergencies.domain.entities import Emergency
from contexts.incidents.emergencies.domain.entities import (
    EmergencyFinder as EmergencyFinderDomain,
)
from contexts.incidents.emergencies.domain.entities import EmergencyRepository
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId


class EmergencyFinder:
    def __init__(self, repository: EmergencyRepository):
        self._finder = EmergencyFinderDomain(repository)

    async def __call__(self, _id: EmergencyId) -> Emergency:
        emergency = await self._finder(_id)
        return emergency
