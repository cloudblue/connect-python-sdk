# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import Schema, fields, post_load

from .base import BaseModel, BaseSchema


class Hub(BaseModel):
    pass


class HubSchema(BaseSchema):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Hub(**data)


class HubsSchemaMixin(Schema):
    hub = fields.Nested(HubSchema, only=('id', 'name'))
    external_id = fields.Int()
