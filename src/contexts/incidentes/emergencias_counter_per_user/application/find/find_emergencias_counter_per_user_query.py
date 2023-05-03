from dataclasses import dataclass

from contexts.shared.domain.bus.query import Query


class FindEmergenciasCounterPerUserQuery(Query):
    def __init__(self, user_id: str):
        self.user_id = user_id
