from contexts.shared.domain.bus.query import Query


class ListEmergenciesQuery(Query):
    def __init__(
        self, filters: str, order_by: str, order_type: str, offset: int, limit: int
    ):
        self.filters = filters
        self.order_by = order_by
        self.order_type = order_type
        self.offset = offset
        self.limit = limit
