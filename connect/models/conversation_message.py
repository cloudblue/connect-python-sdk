# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import datetime

from .base import BaseModel
from .user import User
from .schemas import ConversationMessageSchema


class ConversationMessage(BaseModel):
    """ Message in a :py:class:`.Conversation`. """

    _schema = ConversationMessageSchema()

    conversation = None  # type: str
    """ (str) Primary ID of Conversation object. """

    created = None  # type: datetime.datetime
    """ (datetime.datetime) Date of the Message creation. """

    creator = None  # type: User
    """ (:py:class:`.User`) :py:class:`.User` that created the message. """

    text = None  # type: str
    """ (str) Actual message. """
