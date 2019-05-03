# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import fields, post_load
from typing import List, Optional, Union

from .base import BaseModel, BaseSchema


class ProductConfiguration(BaseModel):
    suspend_resume_supported = None  # type: bool
    requires_reseller_information = None  # type: bool


class ProductConfigurationSchema(BaseSchema):
    suspend_resume_supported = fields.Bool()
    requires_reseller_information = fields.Bool()

    @post_load
    def make_object(self, data):
        return ProductConfiguration(**data)


class DownloadLink(BaseModel):
    title = None  # type: str
    url = None  # type: str


class DownloadLinkSchema(BaseSchema):
    title = fields.Str()
    url = fields.Str()

    @post_load
    def make_object(self, data):
        return DownloadLink(**data)


class Document(BaseModel):
    title = None  # title: str
    url = None  # title: str
    visible_for = None  # title: str


class DocumentSchema(BaseSchema):
    title = fields.Str()
    url = fields.Str()
    visible_for = fields.Str()

    @post_load
    def make_object(self, data):
        return Document(**data)


class CustomerUiSettings(BaseModel):
    description = None  # type: str
    getting_started = None  # type: str
    download_links = None  # type: List[DownloadLink]
    documents = None  # type: List[Document]


class CustomerUiSettingsSchema(BaseSchema):
    description = fields.Str()
    getting_started = fields.Str()
    download_links = fields.Nested(DownloadLinkSchema, many=True)
    documents = fields.Nested(DocumentSchema, many=True)

    @post_load
    def make_object(self, data):
        return CustomerUiSettings(**data)


class Product(BaseModel):
    """ Represents basic marketing information about salable items, parameters, configurations,
    latest published version and connections.

    It contains basic product information like name, description and logo, along with the latest
    published version details. So in a single point we can say a single product object always
    represent the latest published version of that product.
    """

    name = None  # type: str
    """ (str) Product name. """

    icon = None  # type: str
    """ (str) Product icon URI. """

    short_description = None  # type: str
    """ (str) Short description of product. """

    detailed_description = None  # type: str
    """ (str) Detailed description of product. """

    version = None  # type: int
    """ (int) Version of product. """

    configurations = None  # type: ProductConfiguration
    """ (:py:class:`.ProductConfiguration`) Product configuration. """


class ProductSchema(BaseSchema):
    name = fields.Str()
    icon = fields.Str()
    short_description = fields.Str()
    detailed_description = fields.Str()
    version = fields.Int()
    configurations = fields.Nested(ProductConfigurationSchema)

    @post_load
    def make_object(self, data):
        return Product(**data)


class Renewal(BaseModel):
    from_ = None  # type: str
    to = None  # type: str
    period_delta = None  # type: int
    period_uom = None  # type: str


class RenewalSchema(BaseSchema):
    from_ = fields.Str(attribute='from')
    to = fields.Str()
    period_delta = fields.Int()
    period_uom = fields.Str()

    @post_load
    def make_object(self, data):
        return Renewal(**data)


class Item(BaseModel):
    mpn = None  # type: str
    quantity = None  # type: Union[int, str]
    old_quantity = None  # type: Optional[int]
    renewal = None  # type: Optional[Renewal]
    global_id = None  # type: str


class ItemSchema(BaseSchema):
    mpn = fields.Str()
    quantity = fields.Str()
    old_quantity = fields.Integer(allow_none=True)
    renewal = fields.Nested(RenewalSchema, allow_none=True)
    global_id = fields.Str()

    @post_load
    def make_object(self, data):
        # If quantity string contains a number, convert to int
        if 'quantity' in data:
            quantity = data['quantity']
            if quantity.isdigit() or (quantity.startswith('-') and quantity[1:].isdigit()):
                data['quantity'] = int(quantity)
        return Item(**data)
