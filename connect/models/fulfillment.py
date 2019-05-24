# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import datetime

from .asset import Asset
from .base import BaseModel
from .marketplace import Contract, Marketplace
from connect.models.schemas import FulfillmentSchema


class Fulfillment(BaseModel):
    """ Represents a request for the :py:class:`connect.resource.FulfillmentAutomation`
    resource.
    """

    _schema = FulfillmentSchema()

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
        # type: (str) -> bool
        return self.asset.get_param_by_id(migration_key) is not None
