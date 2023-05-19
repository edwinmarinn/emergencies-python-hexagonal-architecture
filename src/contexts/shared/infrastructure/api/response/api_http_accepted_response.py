from http import HTTPStatus
from typing import Mapping

from contexts.shared.domain.value_objects import Uuid

from .api_http_response import ApiHttpResponse


class ApiHttpAcceptedResponse(ApiHttpResponse):
    def __init__(
        self,
        current_url: str,
        request_id: Uuid,
        headers: Mapping[str, str] | None = None,
    ):
        headers = headers or {}
        super().__init__(
            [],
            HTTPStatus.ACCEPTED,
            {"Location": f"{current_url}/status/{request_id.value}", **headers},
        )
