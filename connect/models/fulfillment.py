# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.
import datetime

from marshmallow import fields, post_load

from connect.models import Company
from .asset import Asset, AssetSchema
from .base import BaseModel, BaseSchema
from .marketplace import Contract, ContractSchema, Marketplace, MarketplaceSchema


class Fulfillment(BaseModel):
    """ Represents a request for the :py:class:`connect.resource.FulfillmentAutomation`
    resource.
    """

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

    params_from_url = None  # type: str
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


class FulfillmentSchema(BaseSchema):
    activation_key = fields.Str()
    asset = fields.Nested(AssetSchema)
    status = fields.Str()
    type = fields.Str()
    updated = fields.DateTime()
    created = fields.DateTime()
    reason = fields.Str()
    note = fields.Str()
    params_form_url = fields.Str()
    contract = fields.Nested(ContractSchema, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'))

    @post_load
    def make_object(self, data):
        return Fulfillment(**data)
