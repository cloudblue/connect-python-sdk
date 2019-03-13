# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load
from typing import List

from .base import BaseModel, BaseSchema
from .connection import Connection, ConnectionSchema
from .parameters import Param, ParamSchema
from .product import Item, ItemSchema, Product, ProductSchema
from .tiers import Tiers, TiersSchema


class Asset(BaseModel):
    status = None  # type: str
    external_id = None  # type: str
    external_uid = None  # type: str
    product = None  # type: Product
    connection = None  # type: Connection
    items = None  # type: List[Item]
    params = None  # type: List[Param]
    tiers = None  # type: Tiers

    def get_param_by_id(self, id_):
        try:
            return list(filter(lambda param: param.id == id_, self.params))[0]
        except IndexError:
            return None

    def get_item_by_mpn(self, mpn):
        try:
            return list(filter(lambda item: item.mpn == mpn, self.items))[0]
        except IndexError:
            return None


class AssetSchema(BaseSchema):
    status = fields.Str()
    external_id = fields.Str()
    external_uid = fields.UUID()
    product = fields.Nested(ProductSchema, only=('id', 'name'))
    connection = fields.Nested(
        ConnectionSchema, only=('id', 'type', 'provider', 'vendor'),
    )
    items = fields.List(fields.Nested(ItemSchema))
    params = fields.List(fields.Nested(ParamSchema))
    tiers = fields.Nested(TiersSchema)

    @post_load
    def make_object(self, data):
        return Asset(**data)
