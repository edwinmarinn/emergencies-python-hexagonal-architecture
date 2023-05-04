from dataclasses import dataclass

from contexts.shared.domain.bus.query import Response


@dataclass(frozen=True)
class EmergencyResponse(Response):
    id: str
    code: str
    abscissa: int
    user_id: str
