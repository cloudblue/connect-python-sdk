# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import StatSchema


class Stat(BaseModel):
    """ Stats object. """

    _schema = StatSchema()

    count = None  # type: int
    """ (Int) Count. """

    last_request = None  # type: last_request
    """ (:py:class:`.LastRequest`) Last Request. """
