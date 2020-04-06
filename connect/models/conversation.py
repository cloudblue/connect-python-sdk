# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import datetime

from typing import List

from .base import BaseModel
from .conversation_message import ConversationMessage
from .user import User
from .schemas import ConversationSchema


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

    creator = None  # type: User
    """ (:py:class:`.User`) Creator of the conversation. """

    def add_message(self, message, config=None):
        """ Adds a message to the conversation.

        :param str message: Message to add.
        :param Config config: Configuration, or ``None`` to use the environment config (default).
        :return: The added message.
        :rtype: ConversationMessage
        :raises TypeError: Raised if the message cannot be deserialized.
        """

        from connect.resources.base import ApiClient

        response, _ = ApiClient(config, base_path='conversations/' + self.id + '/messages')\
            .post(json={'text': message})
        return ConversationMessage.deserialize(response)
