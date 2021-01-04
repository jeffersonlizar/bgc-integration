import base64
import json
import logging
from json import JSONDecodeError
from os import getenv

import sentry_sdk
from flask import Flask, jsonify, request

from integration.rest_service.adapters import BackgroundCheckClientAdapter
from integration.rest_service.data_classes import CheckData, ErrorDetail, Response
from integration.rest_service.exceptions import UnauthorizedSatelliteException
from integration.rest_service.providers.exceptions import GenericAPIException

logger = logging.getLogger(__name__)


ENVIRONMENT = getenv("FLASK_ENVIRONMENT", "local")
SENTRY_DSN = getenv("SENTRY_DSN", None)

if SENTRY_DSN:
    sentry_sdk.init(
        SENTRY_DSN,
        environment=ENVIRONMENT,
    )


def run_app(cls):
    assert issubclass(
        cls, BackgroundCheckClientAdapter
    ), "adapter requires to extend from BackgroundCheckClientAdapter class"
    background_check_adapter = cls()
    app = Flask(__name__)

    def get_logger_data(data, message=None):
        data = {
            "data": {
                "provider": background_check_adapter.name,
                "shopper_email": data.email,
            }
        }
        if message:
            try:
                data["data"]["detail"] = json.loads(message)
            except (TypeError, JSONDecodeError):
                data["data"]["detail"] = str(message)

        return data

    def get_error_response(e, code):
        try:
            error_message = e.error_message.decode()
        except AttributeError:
            error_message = e.error_message

        return (
            jsonify(
                Response(
                    error_details=[
                        ErrorDetail(code=e.error_code, message=error_message)
                    ],
                )
            ),
            code,
        )

    def get_check_data(data):
        return CheckData(
            first_name=data.get("first_name"),
            middle_names=data.get("middle_names"),
            no_middle_name=data.get("no_middle_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            dni=data.get("dni"),
            birthdate=data.get("birthdate"),
            social_security_number=data.get("social_security_number"),
            zip_code=data.get("zip_code"),
            driver_license_number=data.get("driver_license_number"),
            driver_license_state=data.get("driver_license_state"),
            phone=data.get("phone"),
            state_code=data.get("state_code"),
            city_name=data.get("city_name"),
            city_code=data.get("city_code"),
            transportation=data.get("transportation"),
            start_url=data.get("start_url"),
            external_id=data.get("external_id"),
            candidate_id=data.get("candidate_id"),
        )

    def validate_request(signature):
        password = str(base64.b64decode(signature), "utf-8")

        if not password == getenv("REQUEST_PASSWORD"):
            raise UnauthorizedSatelliteException(
                error_message="Satellite unauthorized exception"
            )

    @app.route("/create_check", methods=["POST"])
    def create_check():
        try:
            validate_request(request.headers.get("Authorization"))
        except UnauthorizedSatelliteException as e:
            return get_error_response(e, 403)

        data = json.loads(request.data)
        check_data = get_check_data(data)

        try:
            response_data = background_check_adapter.create_check(data=check_data)
            return jsonify(response_data)
        except GenericAPIException as e:
            logger.info(
                f"BGC request error {e.error_message}",
                extra=get_logger_data(check_data, e.error_message),
            )
            return get_error_response(e, 400)

    @app.route("/get_check", methods=["POST"])
    def get_check():
        try:
            validate_request(request.headers.get("Authorization"))
        except UnauthorizedSatelliteException as e:
            return get_error_response(e, 403)

        data = json.loads(request.data)
        check_data = get_check_data(data)

        try:
            response_data = background_check_adapter.get_check(data=check_data)
            return jsonify(response_data)
        except GenericAPIException as e:
            logger.info(
                f"BGC request error {e.error_message}",
                extra=get_logger_data(check_data, e.error_message),
            )
            return get_error_response(e, 400)

    @app.route("/webhook", methods=["POST"])
    def webhook():
        request_status = background_check_adapter.register_webhook_event(request)

        return {}, request_status

    @app.route("/healthz", methods=["GET"])
    def health():
        return {}, 200

    # External integration's health
    @app.route("/external_health", methods=["GET"])
    def external_health():
        if background_check_adapter.external_service_is_healthy():
            return {}, 200
        return {}, 503

    return app
