from http import HTTPStatus

from .api_http_response import ApiHttpResponse


class ApiHttpOkResponse(ApiHttpResponse):
    def __init__(self, data=None, headers: dict[str, str] | None = None):
        super().__init__(data, HTTPStatus.OK, headers)
