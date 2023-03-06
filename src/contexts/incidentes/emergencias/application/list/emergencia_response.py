from dataclasses import dataclass

from contexts.shared.domain.bus.query import Response


@dataclass(frozen=True)
class EmergenciaResponse(Response):
    id: str
    code: str
    abscisa: int
    usuario_id: str
