from dataclasses import dataclass

from domain.shared.bus.command import Command


@dataclass(frozen=True)
class CreateEmergenciaCommand(Command):
    id: str
    code: str
    abscisa: int
    usuario_id: str
