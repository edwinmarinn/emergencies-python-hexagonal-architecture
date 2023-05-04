from contexts.incidents.emergencies.domain.value_objects import EmergencyAbscissa
from contexts.incidents.shared.domain.emergencies.value_objects import EmergencyId
from contexts.incidents.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.command import CommandHandler

from .create_emergency_command import CreateEmergencyCommand
from .emergency_creator import EmergencyCreator


class CreateEmergencyCommandHandler(CommandHandler):
    def __init__(self, creator: EmergencyCreator):
        self._creator = creator

    async def __call__(self, command: CreateEmergencyCommand):
        _id = EmergencyId(command.id)
        abscissa = EmergencyAbscissa(command.abscissa)
        user_id = UserId(command.user_id)

        await self._creator.create(_id=_id, abscissa=abscissa, user_id=user_id)
