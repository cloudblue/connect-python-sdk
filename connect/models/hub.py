# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import Schema, fields, post_load

from .base import BaseModel, BaseSchema


class Hub(BaseModel):
    name = None  # type: str


class HubSchema(BaseSchema):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Hub(**data)


class Hubs(BaseModel):
    hub = None  # type: Hub
    external_id = None  # type: str


class HubsSchema(Schema):
    hub = fields.Nested(HubSchema, only=('id', 'name'))
    external_id = fields.Str()

    @post_load
    def make_object(self, data):
        return Hubs(**data)
