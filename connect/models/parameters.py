# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import Schema, fields, post_load
from typing import List

from .base import BaseModel, BaseSchema


class ValueChoice(BaseModel):
    value = None  # type: str
    label = None  # type: str


class ValueChoiceSchema(Schema):
    value = fields.Str()
    label = fields.Str()

    @post_load
    def make_object(self, data):
        return ValueChoice(**data)


class Param(BaseModel):
    name = None  # type: str
    type = None  # type: str
    value = None  # type: str
    value_choices = None  # type: List[ValueChoice]
    value_error = None  # type: str


class ParamSchema(BaseSchema):
    name = fields.Str()
    type = fields.Str()
    value = fields.Str()
    value_choices = fields.List(fields.Nested(ValueChoiceSchema))
    value_error = fields.Str()

    @post_load
    def make_object(self, data):
        return Param(**data)
