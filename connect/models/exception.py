# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from typing import List, Dict, Any, Optional

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


class UsageFileAction(Message):
    def __init__(self, message, code, data=None):
        # type: (str, str, Optional[Dict[str, Any]]) -> None
        super(UsageFileAction, self).__init__(message, code, data)


class AcceptUsageFile(UsageFileAction):
    def __init__(self, acceptance_note):
        # type: (str) -> None
        super(AcceptUsageFile, self).__init__(
            'Accept Response is required',
            'accept',
            {'acceptance_note': acceptance_note})


class CloseUsageFile(UsageFileAction):
    def __init__(self, message=None):
        # type: (str) -> None
        super(CloseUsageFile, self).__init__(message or 'Usage File Closed', 'close')


class DeleteUsageFile(UsageFileAction):
    def __init__(self, message=None):
        # type: (str) -> None
        super(DeleteUsageFile, self).__init__(message or 'Usage File Deleted', 'delete')


class RejectUsageFile(UsageFileAction):
    def __init__(self, message=None):
        # type: (str) -> None
        super(RejectUsageFile, self).__init__(message or 'Accept Response is required', 'reject')


class SubmitUsageFile(UsageFileAction):
    def __init__(self, rejection_note):
        # type: (str) -> None
        super(SubmitUsageFile, self).__init__(
            'Usage File Submited',
            'submit',
            {'rejection_note': rejection_note})


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


class FileCreationError(Message):
    def __init__(self, message):
        # type: (str) -> None
        super(FileCreationError, self).__init__(message, 'filecreation')


class FileRetrievalError(Message):
    def __init__(self, message):
        # type: (str) -> None
        super(FileRetrievalError, self).__init__(message, 'fileretrieval')
