# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import datetime

from typing import List

from .base import BaseModel
from .company import User
from connect.models.schemas import ConversationMessageSchema, ConversationSchema


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


class Conversation(BaseModel):
    """ Conversation. """

    _schema = ConversationSchema()

    instance_id = None  # type: str
    """ (str)  The id of object based on which discussion is made, e.g. listing request.
    It can be any object.
    """

    created = None  # type: datetime.datetime
    """ (datetime.datetime) Date of the Conversation creation. """

    topic = None  # type: str
    """ (str) Conversation topic. """

    messages = None  # type: List[ConversationMessage]
    """ (List[:py:class:`.ConversationMessage`]) List of :py:class:`.ConversationMessage`
    objects.
    """

    def add_message(self, message, config=None):
        """ Adds a message to the conversation.

        :param str message: Message to add.
        :param Config config: Configuration, or ``None`` to use the environment config (default).
        :return: The added message.
        :rtype: ConversationMessage
        """

        from connect.resources.base import ApiClient
        response, _ = ApiClient(config, base_path='conversations/' + self.id + '/messages')\
            .post(json={'text': message})
        return ConversationMessage.deserialize(response)
