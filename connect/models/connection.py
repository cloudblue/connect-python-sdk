# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema
from .company import Company, CompanySchema
from .hub import Hub, HubSchema
from .product import Product, ProductSchema


class Connection(BaseModel):
    type = None  # type: str
    provider = None  # type: Company
    vendor = None  # type: Company
    product = None  # type: Product
    hub = None  # type: Hub


class ConnectionSchema(BaseSchema):
    type = fields.Str()
    provider = fields.Nested(CompanySchema, only=('id', 'name'))
    vendor = fields.Nested(CompanySchema, only=('id', 'name'))
    product = fields.Nested(ProductSchema)
    hub = fields.Nested(HubSchema)

    @post_load
    def make_object(self, data):
        return Connection(**data)
