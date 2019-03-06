# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema
from .connection import ConnectionSchema
from .parameters import ParamSchema
from .product import ItemSchema, ProductSchema
from .tiers import TiersSchemaMixin


class Asset(BaseModel):
    def get_parameter_by_id(self, id_):
        try:
            return [a for a in self.params if a.id == id_][0]
        except IndexError:
            return None

    def get_item_by_id(self, id_):
        try:
            return [a for a in self.items if a.id == id_][0]
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
    tiers = fields.Nested(TiersSchemaMixin)

    @post_load
    def make_object(self, data):
        return Asset(**data)
