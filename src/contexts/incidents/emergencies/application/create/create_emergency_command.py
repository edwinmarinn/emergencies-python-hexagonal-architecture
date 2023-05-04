from dataclasses import dataclass

from contexts.shared.domain.bus.command import Command


@dataclass(frozen=True)
class CreateEmergencyCommand(Command):
    id: str
    abscissa: int
    user_id: str
