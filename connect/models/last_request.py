# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import LastRequestSchema


class LastRequest(BaseModel):
    """ Last Request object. """

    _schema = LastRequestSchema()

    type = None  # type: str
    """ (str) Type of last request. """
