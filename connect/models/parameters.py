# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import Schema, fields, post_load
from typing import List, Optional

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


class Constraints(BaseModel):
    hidden = None  # type: bool
    required = None  # type: bool
    choices = None  # type: List[ValueChoice]


class ConstraintsSchema(BaseSchema):
    hidden = fields.Bool()
    required = fields.Bool()
    choices = fields.Nested(ValueChoiceSchema, many=True)

    @post_load
    def make_object(self, data):
        return Constraints(**data)


class Param(BaseModel):
    name = None  # type: str
    description = None  # type: str
    type = None  # type: str
    value = None  # type: str
    value_error = None  # type: Optional[str]
    value_choice = None  # type: Optional[List[str]]

    # Undocumented fields (they appear in PHP SDK)
    title = None  # type: Optional[str]
    scope = None  # type: Optional[str]
    constraints = None  # type: Optional[Constraints]


class ParamSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str()
    type = fields.Str()
    value = fields.Str()
    value_error = fields.Str(allow_none=True)
    value_choice = fields.Str(many=True, allow_none=True)

    # Undocumented fields (they appear in PHP SDK)
    title = fields.Str(allow_none=True)
    scope = fields.Str(allow_none=True)
    constraints = fields.Nested(ConstraintsSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        return Param(**data)
