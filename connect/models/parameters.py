# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import Schema, fields, post_load
from typing import List, Optional

from .base import BaseModel, BaseSchema


class ValueChoiceSchema(Schema):
    value = fields.Str()
    label = fields.Str()

    @post_load
    def make_object(self, data):
        return ValueChoice(**data)


class ConstraintsSchema(BaseSchema):
    hidden = fields.Bool()
    required = fields.Bool()
    choices = fields.Nested(ValueChoiceSchema, many=True)

    @post_load
    def make_object(self, data):
        return Constraints(**data)


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


class ValueChoice(BaseModel):
    """ A value choice for a parameter. """

    _schema = ValueChoiceSchema()

    value = None  # type: str
    """ (str) Value. """

    label = None  # type: str
    """ (str) Label. """


class Constraints(BaseModel):
    """ Parameter constraints. """

    _schema = ConstraintsSchema()

    hidden = None  # type: bool
    """ (bool) Is the parameter hidden? """

    required = None  # type: bool
    """ (bool) Is the parameter required? """

    choices = None  # type: List[ValueChoice]
    """ (List[:py:class:`.ValueChoice`]) Parameter value choices. """


class Param(BaseModel):
    """ Parameters are used in product and asset definitions. """

    _schema = ParamSchema()

    name = None  # type: str
    """ (str) Name of parameter. """

    description = None  # type: str
    """ (str) Description of parameter. """

    type = None  # type: str
    """ (str) Type of parameter. """

    value = None  # type: str
    """ (str) Value of parameter. """

    value_error = None  # type: Optional[str]
    """ (str|None) Error indicated for parameter. """

    value_choice = None  # type: Optional[List[str]]
    """ (List[str]|None) Available choices for parameter. """

    # Undocumented fields (they appear in PHP SDK)
    title = None  # type: Optional[str]
    """ (str|None) Title for parameter. """

    scope = None  # type: Optional[str]
    """ (str|None) Scope of parameter. """

    constraints = None  # type: Optional[Constraints]
    """ (:py:class:`.Constraints` | None) Parameter constraints. """
