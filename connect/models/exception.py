# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from .server_error import ServerError


class Message(Exception):
    def __init__(self, message='', code='', obj=None):
        self.message = message
        self.code = code
        self.obj = obj


class FulfillmentFail(Message):
    def __init__(self, *args, **kwargs):
        super(FulfillmentFail, self).__init__(*args, **kwargs)
        self.message = self.message or 'Request failed'
        self.code = 'fail'


class FulfillmentInquire(Message):
    def __init__(self, *args, **kwargs):
        super(FulfillmentInquire, self).__init__(*args, **kwargs)
        self.message = self.message or 'Correct user input required'
        self.code = 'inquire'
        self.params = kwargs.get('params', [])


class Skip(Message):
    def __init__(self, *args, **kwargs):
        super(Skip, self).__init__(*args, **kwargs)
        self.message = self.message or 'Request skipped'
        self.code = 'skip'


class ServerErrorException(Exception):
    message = 'Server error'

    def __init__(self, error=None, *args, **kwargs):
        if error and isinstance(error, ServerError):
            # noinspection PyUnresolvedReferences
            self.message = str({
                "error_code": error.error_code,
                "params": kwargs.get('params', []),
                "errors": error.errors,
            })

        super(ServerErrorException, self).__init__(self.message, *args)
