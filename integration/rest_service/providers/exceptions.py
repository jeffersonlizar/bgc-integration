class GenericAPIException(Exception):
    def __init__(self, *args, **kwargs):
        self.error_message = kwargs.get("error_message")

    def __str__(self):
        return f"{self.error_message}"


class BadRequestAPIException(GenericAPIException):
    def __init__(self, *args, **kwargs):
        self.error_code = "PROVIDER_BAD_REQUEST_ERROR"


class TimeoutAPIException(GenericAPIException):
    def __init__(self, *args, **kwargs):
        self.error_code = "PROVIDER_TIMEOUT_ERROR"


class UnauthorizedAPIException(GenericAPIException):
    def __init__(self, *args, **kwargs):
        self.error_code = "PROVIDER_UNAUTHORIZED_ERROR"


class ForbiddenAPIException(GenericAPIException):
    def __init__(self, *args, **kwargs):
        self.error_code = "PROVIDER_FORBIDDEN_ERROR"


class NotFoundAPIException(GenericAPIException):
    def __init__(self, *args, **kwargs):
        self.error_code = "PROVIDER_NOT_FOUND_ERROR"


class UnprocessableEntityAPIException(GenericAPIException):
    def __init__(self, *args, **kwargs):
        self.error_code = "PROVIDER_UNPROCESSABLE_ENTITY_ERROR"


class ServiceUnavailableAPIException(GenericAPIException):
    def __init__(self, *args, **kwargs):
        self.error_code = "PROVIDER_SERVICE_UNAVAILABLE_ERROR"
