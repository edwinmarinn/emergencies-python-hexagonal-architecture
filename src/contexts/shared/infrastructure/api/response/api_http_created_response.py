from http import HTTPStatus
from typing import Dict

from .api_http_response import ApiHttpResponse


class ApiHttpCreatedResponse(ApiHttpResponse):
    def __init__(self, data=None, headers: Dict[str, str] = None):
        super().__init__(data, HTTPStatus.CREATED, headers)
