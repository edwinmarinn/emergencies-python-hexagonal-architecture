from contexts.incidentes.emergencias.domain.value_objects import EmergenciaAbscisa
from contexts.incidentes.shared.domain.emergencias.value_objects import EmergenciaId
from contexts.incidentes.shared.domain.value_objects import UserId
from contexts.shared.domain.bus.command import CommandHandler

from .create_emergencia_command import CreateEmergenciaCommand
from .emergencia_creator import EmergenciaCreator


class CreateEmergenciaCommandHandler(CommandHandler):
    def __init__(self, creator: EmergenciaCreator):
        self._creator = creator

    async def __call__(self, command: CreateEmergenciaCommand):
        _id = EmergenciaId(command.id)
        abscisa = EmergenciaAbscisa(command.abscisa)
        user_id = UserId(command.user_id)

        await self._creator.create(_id=_id, abscisa=abscisa, user_id=user_id)
