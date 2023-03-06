from dataclasses import dataclass

from contexts.shared.domain.bus.query import Query


@dataclass
class FindVideoQuery(Query):
    id: str
