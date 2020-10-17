class GenericAPIException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = kwargs.get("message")
        self.status_code = kwargs.get("status_code")

    def __str__(self):
        return "{}".format(self.message)


class BadRequestAPIException(GenericAPIException):
    pass


class UnauthorizedAPIException(GenericAPIException):
    pass


class ForbiddenAPIException(GenericAPIException):
    pass


class NotFoundAPIException(GenericAPIException):
    pass


class UnprocessableEntityAPIException(GenericAPIException):
    pass


class GenericErrorDetailException(GenericAPIException):
    pass


class ImproperlyConfigured(GenericAPIException):
    pass
