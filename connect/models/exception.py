# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from typing import List

from connect.models import Param
from .server_error import ServerError


class Message(Exception):
    code = None  # type: str
    obj = None  # type: object

    def __init__(self, message='', code='', obj=None):
        # type: (str, str, object) -> None
        self.message = message
        self.code = code
        self.obj = obj


class FulfillmentFail(Message):
    def __init__(self, *args, **kwargs):
        # type: (*any, **any) -> None
        super(FulfillmentFail, self).__init__(*args, **kwargs)
        self.message = self.message or 'Request failed'
        self.code = 'fail'


class FulfillmentInquire(Message):
    params = None  # type: List[Param]

    def __init__(self, *args, **kwargs):
        # type: (*any, **any) -> None
        super(FulfillmentInquire, self).__init__(*args, **kwargs)
        self.message = self.message or 'Correct user input required'
        self.code = 'inquire'
        self.params = kwargs.get('params', [])


class Skip(Message):
    def __init__(self, *args, **kwargs):
        # type: (*any, **any) -> None
        super(Skip, self).__init__(*args, **kwargs)
        self.message = self.message or 'Request skipped'
        self.code = 'skip'


class ServerErrorException(Exception):
    message = 'Server error'  # type: str

    def __init__(self, error=None, *args, **kwargs):
        # type: (ServerError, *any, **any) -> None

        if error and isinstance(error, ServerError):
            self.message = str({
                "error_code": error.error_code,
                "params": kwargs.get('params', []),
                "errors": error.errors,
            })
        else:
            self.message = self.__class__.message

        super(ServerErrorException, self).__init__(self.message, *args)
