from dataclasses import dataclass

from contexts.shared.domain.bus.command import Command


@dataclass(frozen=True)
class CreateEmergenciaCommand(Command):
    id: str
    abscisa: int
    user_id: str
