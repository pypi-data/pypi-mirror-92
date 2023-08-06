from __future__ import unicode_literals
from abc import ABCMeta

from future.utils import with_metaclass

class BaseError(with_metaclass(ABCMeta, Exception)):
    def __init__(self, message=""):
        self.message = message

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "{name} | {message}".format(name=self.__class__.__name__, message=self.message)


class ParameterError(BaseError):
    def __init__(self, parameter_name, message):
        super().__init__(message)
        self.parameter_name = parameter_name

    def __str__(self):
        return "error parameter: {parameter_name}, message: {message}".format(parameter_name=self.parameter_name, message=self.message)


class EInvoiceApiError(BaseError):
    def __init__(self, status_code, sub_code, message, request_url=""):
        super().__init__(message)
        self.status_code = status_code
        self.sub_code = sub_code
        self.request_url = request_url

    def __str__(self):
        return "status_code: {status_code}, sub_code: {sub_code}, " \
               "message: {message}, request_url: {request_url}".format(status_code=self.status_code,
                                                                       sub_code=self.sub_code,
                                                                       message=self.message,
                                                                       request_url=self.request_url)


