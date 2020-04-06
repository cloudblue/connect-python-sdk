# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import List

from .base import BaseModel
from .schemas import ServerErrorResponseSchema


class ServerErrorResponse(BaseModel):
    """ Server response when an error occurs. """

    _schema = ServerErrorResponseSchema()

    error_code = None  # type: str
    """ (str) Error code. """

    params = None  # type: dict
    """ (dict) Error params. """

    errors = None  # type: List[str]
    """ (List[str]) List of errors. """

    def __str__(self):
        return str({
            'error_code': self.error_code,
            'params': self.params,
            'errors': self.errors,
        })
