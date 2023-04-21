from contexts.shared.domain import DomainError
from contexts.shared.domain.bus.query import Query


class QueryNotRegisteredError(DomainError):
    def __init__(self, query: Query):
        self._query = query
        super().__init__()

    def error_code(self) -> str:
        return "query_bus_not_registered_error"

    def error_message(self) -> str:
        return f"The query <{type(self._query).__name__}> has not been registered"
