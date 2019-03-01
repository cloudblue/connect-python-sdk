# -*- coding: utf-8 -*-

from marshmallow import fields, post_load

from .asset import AssetSchema
from .base import BaseModel, BaseSchema
from .marketplace import ContractSchema, MarketplaceSchema


class Fulfillment(BaseModel):
    pass


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
