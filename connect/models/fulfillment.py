# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load

from .asset import Asset, AssetSchema
from .base import BaseModel, BaseSchema
from .marketplace import Contract, ContractSchema, Marketplace, MarketplaceSchema


class Fulfillment(BaseModel):
    activation_key = None  # type: str
    asset = None  # type: Asset
    status = None  # type: str
    type = None  # type: str
    updated = None  # type: str
    created = None  # type: str
    reason = None  # type: str
    params_from_url = None  # type: str
    contract = None  # type: Contract
    marketplace = None  # type: Marketplace

    @property
    def new_items(self):
        # noinspection PyUnresolvedReferences
        return list(filter(
            lambda item: item.quantity > 0 and item.old_quantity == 0,
            self.asset.items))

    @property
    def changed_items(self):
        # noinspection PyUnresolvedReferences
        return list(filter(
            lambda item: item.quantity > 0 and item.old_quantity > 0,
            self.asset.items))

    @property
    def removed_items(self):
        # noinspection PyUnresolvedReferences
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
    params_form_url = fields.Str()
    contract = fields.Nested(ContractSchema, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'))

    @post_load
    def make_object(self, data):
        return Fulfillment(**data)
