from http import HTTPStatus

from .api_http_response import ApiHttpResponse


class ApiHttpCreatedResponse(ApiHttpResponse):
    def __init__(self, data=None, headers: dict[str, str] | None = None):
        super().__init__(data, HTTPStatus.CREATED, headers)
