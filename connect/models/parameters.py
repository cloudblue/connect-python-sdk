# -*- coding: utf-8 -*-

from marshmallow import Schema, fields, post_load

from .base import BaseModel, BaseSchema


class ValueChoice(BaseModel):
    pass


class ValueChoiceSchema(Schema):
    value = fields.Str()
    label = fields.Str()

    @post_load
    def make_object(self, data):
        return ValueChoice(**data)


class Param(BaseModel):
    pass


class ParamSchema(BaseSchema):
    name = fields.Str()
    type = fields.Str()
    value = fields.Str()
    value_choices = fields.List(fields.Nested(ValueChoiceSchema))
    value_error = fields.Str()

    @post_load
    def make_object(self, data):
        return Param(**data)
