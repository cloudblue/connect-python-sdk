# -*- coding: utf-8 -*-

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema


class Product(BaseModel):
    pass


class ProductSchema(BaseSchema):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Product(**data)


class Item(BaseModel):
    pass


class ItemSchema(BaseSchema):
    global_id = fields.Str()
    mpn = fields.Str()
    old_quantity = fields.Str()
    quantity = fields.Integer()

    @post_load
    def make_object(self, data):
        return Item(**data)
