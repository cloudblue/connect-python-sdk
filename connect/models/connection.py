# -*- coding: utf-8 -*-

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema
from .company import CompanySchema
from .hub import HubSchema
from .product import ProductSchema


class Connection(BaseModel):
    pass


class ConnectionSchema(BaseSchema):
    type = fields.Str()
    provider = fields.Nested(CompanySchema, only=('id', 'name'))
    vendor = fields.Nested(CompanySchema, only=('id', 'name'))
    product = fields.Nested(ProductSchema)
    hub = fields.Nested(HubSchema)

    @post_load
    def make_object(self, data):
        return Connection(**data)
