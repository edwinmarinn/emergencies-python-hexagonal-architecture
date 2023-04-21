from dataclasses import dataclass
from typing import List

from contexts.shared.domain.bus.query import Response


@dataclass(frozen=True)
class EmergenciaResponse:
    id: str
    code: str
    abscisa: int
    usuario_id: str


class EmergenciasResponse(Response):
    def __init__(self, emergencias: List[EmergenciaResponse]):
        self.emergencias = emergencias
