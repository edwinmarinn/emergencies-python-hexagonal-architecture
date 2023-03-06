class DomainError(Exception):
    def __init__(self):
        super().__init__(self._error_message())

    def error_code(self) -> str:
        raise NotImplementedError

    def _error_message(self) -> str:
        raise NotImplementedError
