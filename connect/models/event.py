# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

import datetime
from typing import Optional

from .base import BaseModel
from .user import User
from .schemas import EventSchema


class Event(BaseModel):
    """ Represents the date and user that caused an event. """

    _schema = EventSchema()

    at = None  # type: Optional[datetime.datetime]
    """ (datetime.datetime|None) Date when the event occurred. """

    by = None  # type: Optional[User]
    """ (:py:class:`.User`) User that caused the event. """
