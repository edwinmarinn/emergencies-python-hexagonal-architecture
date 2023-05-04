from dataclasses import dataclass
from typing import List

from contexts.shared.domain.bus.query import Response


@dataclass(frozen=True)
class EmergencyResponse:
    id: str
    code: str
    abscissa: int
    user_id: str


class EmergenciesResponse(Response):
    def __init__(self, emergencies: List[EmergencyResponse]):
        self.emergencies = emergencies
