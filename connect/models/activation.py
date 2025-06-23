# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

import datetime
from typing import Optional

from .base import BaseModel
from .schemas import ActivationSchema


class Activation(BaseModel):
    """ Activation object. """

    _schema = ActivationSchema()

    link = None  # type: Optional[str]
    """ (str|None) Activation link. """

    message = None  # type: str
    """ (str) Activation message. """

    date = None  # type: Optional[datetime.datetime]
    """ (datetime.datetime|None) Activation date. """
