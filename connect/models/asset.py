from marshmallow import fields, post_load

from .base import BaseObject, BaseScheme
from .connection import ConnectionScheme
from .parameters import ParamsScheme
from .product import ItemScheme, ProductScheme
from .tiers import TiersSchemeMixin


class Asset(BaseObject):
    pass


class AssetScheme(BaseScheme):
    status = fields.Str()
    external_id = fields.Str()
    external_uid = fields.UUID()
    product = fields.Nested(ProductScheme, only=('id', 'name'))
    connection = fields.Nested(
        ConnectionScheme, only=('id', 'type', 'provider', 'vendor'),
    )
    items = fields.List(fields.Nested(ItemScheme))
    params = fields.List(fields.Nested(ParamsScheme))
    tiers = fields.Nested(TiersSchemeMixin)

    @post_load
    def make_object(self, data):
        return Asset(**data)
