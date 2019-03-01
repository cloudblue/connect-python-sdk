from marshmallow import fields, post_load

from .asset import AssetScheme
from .base import BaseObject, BaseScheme
from .marketplace import ContractScheme, MarketplaceScheme


class Fulfillment(BaseObject):
    pass


class FulfillmentScheme(BaseScheme):
    activation_key = fields.Str()
    asset = fields.Nested(AssetScheme)
    status = fields.Str()
    type = fields.Str()
    updated = fields.DateTime()
    created = fields.DateTime()
    reason = fields.Str()
    params_form_url = fields.Str()
    contract = fields.Nested(ContractScheme, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceScheme, only=('id', 'name'))

    @post_load
    def make_object(self, data):
        return Fulfillment(**data)
