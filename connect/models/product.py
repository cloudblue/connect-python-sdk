# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from typing import List, Optional, Union

from marshmallow import fields, post_load
import six

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
    name = None  # type: str
    icon = None  # type: str
    short_description = None  # type: str
    detailed_description = None  # type: str
    version = None  # type: int
    configurations = None  # type: ProductConfiguration


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
    from_ = fields.DateTime(attribute='from')
    to = fields.DateTime()
    period_delta = fields.Int()
    period_uom = fields.Str()

    @post_load
    def make_object(self, data):
        return Renewal(**data)


class Item(BaseModel):
    mpn = None  # type: str
    quantity = None  # type: Union[int,float]
    old_quantity = None  # type: Union[int,float,None]
    renewal = None  # type: Optional[Renewal]
    global_id = None  # type: str


class QuantityField(fields.Field):
    def _deserialize(self, value, attr, obj, **kwargs):
        if isinstance(value, six.string_types):
            if value == 'unlimited':
                return -1
            else:
                try:
                    float_val = float(value)
                    int_val = int(float_val)
                    return int_val if int_val == float_val else float_val
                except ValueError:
                    raise ValueError({
                        attr: [u'Not a valid string encoded number nor "unlimited".']
                    })
        elif isinstance(value, (int, float)):
            return value
        else:
            raise ValueError({attr: [u'Not a valid int, float or string.']})


class ItemSchema(BaseSchema):
    mpn = fields.Str()
    quantity = QuantityField()
    old_quantity = QuantityField(allow_none=True)
    renewal = fields.Nested(RenewalSchema, allow_none=True)
    global_id = fields.Str()

    @post_load
    def make_object(self, data):
        return Item(**data)
