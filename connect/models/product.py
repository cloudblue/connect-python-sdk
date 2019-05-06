# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load
from typing import Union

from .base import BaseModel, BaseSchema


class Product(BaseModel):
    name = None  # type: str
    icon = None  # type: str


class ProductSchema(BaseSchema):
    name = fields.Str()
    icon = fields.Str()

    @post_load
    def make_object(self, data):
        return Product(**data)


class Item(BaseModel):
    global_id = None  # type: str
    mpn = None  # type: str
    old_quantity = None  # type: Union[int, None]
    quantity = None  # type: Union[int, None]


class ItemSchema(BaseSchema):
    global_id = fields.Str()
    mpn = fields.Str()
    old_quantity = fields.Str()
    quantity = fields.Str()

    @post_load
    def make_object(self, data):
        params = ('quantity', 'old_quantity')
        for param in params:
            if param in data:
                value = data[param]
                if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                    data[param] = int(value)
                else:
                    data[param] = None
        return Item(**data)
