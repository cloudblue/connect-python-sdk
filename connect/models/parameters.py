from marshmallow import Schema, fields, post_load

from .base import BaseObject, BaseScheme


class ValueChoice(BaseObject):
    pass


class ValueChoiceScheme(Schema):
    value = fields.Str()
    label = fields.Str()

    @post_load
    def make_object(self, data):
        return ValueChoice(**data)


class Param(BaseObject):
    pass


class ParamsScheme(BaseScheme):
    name = fields.Str()
    type = fields.Str()
    value = fields.Str()
    value_choices = fields.List(fields.Nested(ValueChoiceScheme))
    value_error = fields.Str()

    @post_load
    def make_object(self, data):
        return Param(**data)
