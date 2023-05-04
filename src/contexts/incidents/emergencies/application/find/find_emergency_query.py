from contexts.shared.domain.bus.query import Query


class FindEmergencyQuery(Query):
    def __init__(self, id: str):
        self.id = id
