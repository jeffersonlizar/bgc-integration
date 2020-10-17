# -*- coding: utf-8 -*-
class GenericErrorDetailException(Exception):
    def __init__(self, *args, **kwargs):
        self.message = kwargs.get("message")
        self.code = kwargs.get("code")

    def __str__(self):
        return "{}".format(self.message)


class GenericAPIException(GenericErrorDetailException):
    pass


class BadRequestAPIException(GenericErrorDetailException):
    pass


class UnauthorizedAPIException(GenericErrorDetailException):
    pass


class ForbiddenAPIException(GenericErrorDetailException):
    pass


class NotFoundAPIException(GenericErrorDetailException):
    pass


class UnprocessableEntityAPIException(GenericErrorDetailException):
    pass
