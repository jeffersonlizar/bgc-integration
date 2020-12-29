from typing import Dict, Union

from flask import request

from .data_classes import CheckData, Response


class BackgroundCheckClientAdapter:
    name = None

    def create_check(self, data: CheckData) -> Response:
        raise NotImplementedError

    def create_check_request(self, data: CheckData) -> Dict:
        raise NotImplementedError

    def response_to_check(
        self, data: Dict[str, Union[str, int, Dict[str, int]]], input_data: CheckData
    ) -> Response:
        raise NotImplementedError

    def get_check(self, data: CheckData) -> Response:
        raise NotImplementedError

    def register_webhook_event(self, request: request) -> int:
        raise NotImplementedError

    def external_service_is_healthy(self) -> bool:
        raise NotImplementedError
