from application.emergencia.create import CreateEmergenciaCommand, EmergenciaCreator
from domain.emergencia.value_objects import (
    EmergenciaAbscisa,
    EmergenciaCode,
    EmergenciaId,
)
from domain.shared.bus.command import CommandHandler
from domain.shared.value_objects import UsuarioId


class CreateEmergenciaCommandHandler(CommandHandler):
    def __init__(self, creator: EmergenciaCreator):
        self._creator = creator

    def __call__(self, command: CreateEmergenciaCommand):
        _id = EmergenciaId(command.id)
        code = EmergenciaCode(command.code)
        abscisa = EmergenciaAbscisa(command.abscisa)
        usuario_id = UsuarioId(command.usuario_id)

        self._creator.create(_id=_id, code=code, abscisa=abscisa, usuario_id=usuario_id)
