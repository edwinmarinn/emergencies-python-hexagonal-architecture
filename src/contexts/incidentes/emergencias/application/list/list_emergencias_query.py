from dataclasses import dataclass

from contexts.shared.domain.bus.query import Query


@dataclass
class ListEmergenciasQuery(Query):
    filters: str
    order_by: str
    order_type: str
    offset: int
    limit: int
