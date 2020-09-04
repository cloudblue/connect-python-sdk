# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import List

from deprecation import deprecated
import six

from .models.param import Param


class Message(Exception):
    """ Base class for all Connect exceptions.

    :param str message: Exception message.
    :param str code: Exception code.
    :param object obj: Additional information.
    """

    code = None  # type: str
    """ (str) Exception code. """

    obj = None  # type: object
    """ (str) Additional information. """

    def __init__(self, message='', code='', obj=None):
        # On Python 2, Unicode messages must be utf-8 encoded
        if six.PY2 and isinstance(message, six.string_types) and not isinstance(message, str):
            message = message.encode('utf-8')
        super(Message, self).__init__(message)
        self.code = code
        self.obj = obj

    @property
    @deprecated(deprecated_in='16.0', details='Use ``str(exception)`` instead.')
    def message(self):
        """
        :return: The exception message.
        :rtype: str
        """
        return str(self)


class FailRequest(Message):
    """ Causes the request being processed to fail.

    :param str message: Exception message.
    """
    def __init__(self, message=''):
        super(FailRequest, self).__init__(message or 'Request failed', 'fail')


class InquireRequest(Message):
    """ Causes the request being processed to inquire for some information.

    :param str message: Exception message.
    :param List[Param] params: Parameters to inquire.
    """

    params = None  # type: List[Param]
    """ (List[:py:class:`.Param`]) Parameters to inquire. """

    def __init__(self, message='', params=None):
        super(InquireRequest, self).__init__(message or 'Correct user input required', 'inquire')
        self.params = params or []


class SkipRequest(Message):
    """ Causes the request being processed to be skipped.

    :param str message: Exception message.
    """

    def __init__(self, message=''):
        super(SkipRequest, self).__init__(message or 'Request skipped', 'skip')


class ServerError(Exception):
    """ Indicates that the server returned an error.

    :param ServerErrorResponse error: Response returned by the server.
    """

    def __init__(self, error):
        self.error = error
        super(ServerError, self).__init__(str(error), error.error_code)


class UsageFileAction(Message):
    """ Base exception for Usage API actions.

    :param str message: Exception message.
    :param str code: Exception code.
    :param Optional[Dict[str,Any]] data: Additional information.
    """

    def __init__(self, message, code, data=None):
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
    def __init__(self, rejection_note):
        # type: (str) -> None
        super(RejectUsageFile, self).__init__(
            'Reject Response is required',
            'reject',
            {'rejection_note': rejection_note})


class SubmitUsageFile(UsageFileAction):
    def __init__(self):
        # type: () -> None
        super(SubmitUsageFile, self).__init__('Usage File Submitted', 'submit', {})


class FileCreationError(Message):
    def __init__(self, message):
        # type: (str) -> None
        super(FileCreationError, self).__init__(message, 'filecreation')


class FileRetrievalError(Message):
    def __init__(self, message):
        # type: (str) -> None
        super(FileRetrievalError, self).__init__(message, 'fileretrieval')
