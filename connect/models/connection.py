# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema
from .company import Company, CompanySchema
from .hub import Hub, HubSchema
from .product import Product, ProductSchema


class Connection(BaseModel):
    """ Represents a communication channel which provides the ability
    to order pr oducts within particular hub.

    Standalone connection is required for each product and for each provider account.
    """

    type = None  # type: str
    """ (str) Type of connection. """

    provider = None  # type: Company
    """ (:py:class:`.Company`) Provider Account Reference. """

    vendor = None  # type: Company
    """ (:py:class:`.Company`) Vendor Account Reference. """

    product = None  # type: Product
    """ (:py:class:`.Product`) Product Reference. """

    hub = None  # type: Hub
    """ (:py:class:`.Hub`) Hub Reference. """


class ConnectionSchema(BaseSchema):
    type = fields.Str()
    provider = fields.Nested(CompanySchema, only=('id', 'name'))
    vendor = fields.Nested(CompanySchema, only=('id', 'name'))
    product = fields.Nested(ProductSchema)
    hub = fields.Nested(HubSchema)

    @post_load
    def make_object(self, data):
        return Connection(**data)
