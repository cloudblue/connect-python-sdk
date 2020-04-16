# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.
from .base import BaseModel
from .event import Event
from .schemas import EventsSchema


class Events(BaseModel):
    """ Represents a set of events that can take place on an object. """

    _schema = EventsSchema()

    created = None  # type: Event
    """ (:py:class:`.EventInfo`) Creation event. """

    inquired = None  # type: Event
    """ (:py:class:`.EventInfo`) Inquire event. """

    pended = None  # type: Event
    """ (:py:class:`.EventInfo`) Pending event. """

    validated = None  # type: Event
    """ (:py:class:`.EventInfo`) Validation event. """

    updated = None  # type: Event
    """ (:py:class:`.EventInfo`) Update event. """

    approved = None  # type: Event
    """ (:py:class:`.EventInfo`) Approve event. """

    uploaded = None  # type: Event
    """ (:py:class:`.EventInfo`) Uploaded event. """

    submitted = None  # type: Event
    """ (:py:class:`.EventInfo`) Submit event. """

    accepted = None  # type: Event
    """ (:py:class:`.EventInfo`) Accept event. """

    rejected = None  # type: Event
    """ (:py:class:`.EventInfo`) Reject event. """

    closed = None  # type: Event
    """ (:py:class:`.EventInfo`) Close event. """
