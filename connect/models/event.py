# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import datetime
from typing import Optional

from .base import BaseModel
from .company import User
from connect.models.schemas import EventInfoSchema, EventsSchema


class EventInfo(BaseModel):
    """ Represents the date and user that caused an event. """

    _schema = EventInfoSchema()

    at = None  # type: Optional[datetime.datetime]
    """ (datetime.datetime|None) Date when the event occurred. """

    by = None  # type: Optional[User]
    """ (:py:class:`.User`) User that caused the event. """


class Events(BaseModel):
    """ Represents a set of events that can take place on an object. """

    _schema = EventsSchema()

    created = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Creation event. """

    inquired = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Inquire event. """

    pended = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Pending event. """

    validated = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Validation event. """

    updated = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Update event. """

    approved = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Approve event. """

    uploaded = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Uploaded event. """

    submitted = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Submit event. """

    accepted = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Accept event. """

    rejected = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Reject event. """

    closed = None  # type: EventInfo
    """ (:py:class:`.EventInfo`) Close event. """
