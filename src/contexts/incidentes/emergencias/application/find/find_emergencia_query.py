from dataclasses import dataclass

from contexts.shared.domain.bus.query import Query


@dataclass
class FindEmergenciaQuery(Query):
    id: str
