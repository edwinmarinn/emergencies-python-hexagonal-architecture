from contexts.shared.domain.bus.query import Query


class FindEmergenciaQuery(Query):
    def __init__(self, id: str):
        self.id = id
