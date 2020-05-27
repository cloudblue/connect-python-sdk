# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import datetime
from typing import Union

from .asset import Asset
from .base import BaseModel
from .contract import Contract
from .conversation import Conversation
from .marketplace import Marketplace
from .user import User
from .schemas import AssetRequestSchema


class AssetRequest(BaseModel):
    """ Represents a request for the :py:class:`connect.resource.FulfillmentAutomation`
    resource.
    """

    _schema = AssetRequestSchema()

    type = None  # type: str
    """ (str) Asset status. See :py:class:`.Asset` class for details. """

    created = None  # type: datetime.datetime
    """ (datetime.datetime) Date of request creation. """

    updated = None  # type: datetime.datetime
    """ (datetime.datetime) Date of last request modification. """

    status = None  # type: str
    """ (str) Status of request. One of:

    - pending
    - inquiring
    - failed
    - approved

    Valid status changes:

    - pending -> inquiring
    - pending -> failed
    - pending -> approved
    - inquiring -> failed
    - inquiring -> approved
    - inquiring -> pending
    """

    params_form_url = None  # type: str
    """ (str) URL for customer/reseller/provider for modifying param value
    based on vendor's feedback.
    """

    activation_key = None  # type: str
    """ (str) Activation key content for activating the subscription on vendor portal.
    This markdown formatted message is sent to customer.
    """

    reason = None  # type: str
    """ (str) Fail reason in case of status of request is failed. """

    note = None  # type: str
    """ (str) Details of note. """

    asset = None  # type: Asset
    """ (:py:class:`.Asset`) Asset object. """

    contract = None  # type: Contract
    """ (:py:class:`.Contract`) Contract object. """

    marketplace = None  # type: Marketplace
    """ (:py:class:`.Marketplace`) Marketplace object. """

    assignee = None  # type: Union[User, str, None]
    """ (:py:class:`.User` | None) Details of the user assigned to the request. """

    @property
    def new_items(self):
        """
        :return: New items.
        :rtype: List[Item]
        """
        return list(filter(
            lambda item: item.quantity > 0 and item.old_quantity == 0,
            self.asset.items))

    @property
    def changed_items(self):
        """
        :return: Changed items.
        :rtype: List[Item]
        """
        return list(filter(
            lambda item: item.quantity > 0 and item.old_quantity > 0,
            self.asset.items))

    @property
    def removed_items(self):
        """
        :return: Removed items.
        :rtype: List[Item]
        """
        return list(filter(
            lambda item: item.quantity == 0 and item.old_quantity > 0,
            self.asset.items))

    def needs_migration(self, migration_key='migration_info'):
        """
        Indicates whether the request contains data to be migrated from a legacy product.
        Migration is performed by an external service. All you have to do for a request that
        needs migration is to skip processing by raising a
        :py:class:`connect.exceptions.SkipRequest` exception.

        :param str migration_key: The name of the parameter that contains the migration data
            (optional; default value is ``migration_info``).
        :return: Whether the request needs migrating.
        :rtype: bool
        """
        param = self.asset.get_param_by_id(migration_key)
        return param is not None and bool(param.value)

    def get_conversation(self, config=None):
        """
        :param Config config: Configuration, or ``None`` to use the environment config (default).
        :return: The conversation for this request, or ``None`` if there is none.
        :rtype: Conversation|None
        """
        from connect.resources.base import ApiClient

        client = ApiClient(config, base_path='conversations')
        response, _ = client.get(params={'instance_id': self.id})
        try:
            conversations = Conversation.deserialize(response)
            if conversations and conversations[0].id:
                response, _ = client.get(conversations[0].id)
                return Conversation.deserialize(response)
            else:
                return None
        except ValueError:
            return None
