from http import HTTPStatus


class ApiExceptionsHttpStatusCodeMapping:
    def __init__(self):
        self._exceptions: dict[str, int] = {
            ValueError.__name__: HTTPStatus.BAD_REQUEST,
        }

    def register(self, exception_class: str, status_code: int) -> None:
        self._exceptions[exception_class] = status_code

    def exists(self, exception_class: str) -> bool:
        return exception_class in self._exceptions

    def get_status_code(self, exception_class: str) -> int:
        return self._exceptions[exception_class]
