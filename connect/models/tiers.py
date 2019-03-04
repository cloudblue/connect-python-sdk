# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import Schema, fields, post_load

from .base import BaseModel, BaseSchema


class Tier(BaseModel):
    pass


class TierSchema(BaseSchema):
    name = fields.Str()
    contact_info = fields.Dict()
    external_id = fields.Str()
    external_uid = fields.UUID()

    @post_load
    def make_object(self, data):
        return Tier(**data)


class TiersSchemaMixin(Schema):
    customer = fields.Nested(TierSchema)
    tier1 = fields.Nested(TierSchema)
    tier2 = fields.Nested(TierSchema)
