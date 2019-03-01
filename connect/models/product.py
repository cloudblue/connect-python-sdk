from marshmallow import fields, post_load

from .base import BaseObject, BaseScheme


class Product(BaseObject):
    pass


class ProductScheme(BaseScheme):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Product(**data)


class Item(BaseObject):
    pass


class ItemScheme(BaseScheme):
    global_id = fields.Str()
    mpn = fields.Str()
    old_quantity = fields.Str()
    quantity = fields.Integer()

    @post_load
    def make_object(self, data):
        return Item(**data)
