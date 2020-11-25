import base64
import json
import logging
import sentry_sdk
from json import JSONDecodeError
from os import getenv

from flask import Flask, jsonify, request
from requests import Timeout

from integration.rest_service.adapters import BackgroundCheckClientAdapter
from integration.rest_service.constants import FAILED
from integration.rest_service.data_classes import CheckData, ErrorDetail, Response
from integration.rest_service.providers.exceptions import (
    BadRequestAPIException,
    GenericAPIException,
    NotFoundAPIException,
)

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

    @app.route("/create_check", methods=["POST"])
    def create_check():
        signature = request.headers.get("Authorization")
        password = str(base64.b64decode(signature), "utf-8")

        if password != getenv("REQUEST_PASSWORD"):
            return json.dumps({"success": False}), 403

        data = json.loads(request.data)
        check_data = CheckData(
            first_name=data.get("first_name"),
            middle_names=data.get("middle_names"),
            no_middle_name=data.get("no_middle_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
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
        try:
            response_data = background_check_adapter.create_check(data=check_data)
        except (Timeout, ConnectionError):
            logger.info("BGC adapter timeout", extra=get_logger_data(check_data))
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(
                            code="408", message=json.loads({"error": "Timeout"})
                        )
                    ],
                )
            )
        except (BadRequestAPIException, NotFoundAPIException) as e:
            logger.info(
                "BGC adapter request exception",
                extra=get_logger_data(check_data, e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="400", message=json.loads(e.message))
                    ],
                )
            )
        except GenericAPIException as e:
            logger.info(
                "BGC adapter generic exception",
                extra=get_logger_data(check_data, e.message),
            )
            return jsonify(
                Response(
                    status=FAILED,
                    error_details=[
                        ErrorDetail(code="500", message=json.loads(e.message))
                    ],
                )
            )
        return response_data

    @app.route("/get_check", methods=["POST"])
    def get_check():
        signature = request.headers.get("Authorization")
        password = str(base64.b64decode(signature), "utf-8")

        if password != getenv("REQUEST_PASSWORD"):
            return json.dumps({"success": False}), 403

        data = json.loads(request.data)
        check_data = CheckData(
            first_name=data.get("first_name"),
            middle_names=data.get("middle_names"),
            no_middle_name=data.get("no_middle_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
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
        response_data = background_check_adapter.get_check(data=check_data)
        return response_data

    @app.route("/webhook", methods=["POST"])
    def webhook():
        request_status = background_check_adapter.register_webhook_event(request)

        if request_status == 200:
            return json.dumps({"success": True}), 200
        else:
            return json.dumps({"success": False}), request_status

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
