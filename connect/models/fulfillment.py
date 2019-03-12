# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load

from .asset import AssetSchema
from .base import BaseModel, BaseSchema
from .marketplace import ContractSchema, MarketplaceSchema


class Fulfillment(BaseModel):
    @property
    def new_items(self):
        return filter(lambda item: item.quantity > 0 and item.old_quantity == 0, self.asset.items)

    @property
    def changed_items(self):
        return filter(lambda item: item.quantity > 0 and item.old_quantity > 0, self.asset.items)

    @property
    def removed_items(self):
        return filter(lambda item: item.quantity == 0 and item.old_quantity > 0, self.asset.items)


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
