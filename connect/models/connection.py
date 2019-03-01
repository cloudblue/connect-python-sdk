from marshmallow import fields, post_load

from .base import BaseObject, BaseScheme
from .company import CompanyScheme
from .hub import HubScheme
from .product import ProductScheme


class Connection(BaseObject):
    pass


class ConnectionScheme(BaseScheme):
    type = fields.Str()
    provider = fields.Nested(CompanyScheme, only=('id', 'name'))
    vendor = fields.Nested(CompanyScheme, only=('id', 'name'))
    product = fields.Nested(ProductScheme)
    hub = fields.Nested(HubScheme)

    @post_load
    def make_object(self, data):
        return Connection(**data)
