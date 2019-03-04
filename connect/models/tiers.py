# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import Schema, fields, post_load

from .base import BaseModel, BaseSchema


class Tier(BaseModel):
    name = None  # type: str
    contract_info = None  # type: dict
    external_id = None  # type: str
    external_uid = None  # type: str


class TierSchema(BaseSchema):
    name = fields.Str()
    contact_info = fields.Dict()
    external_id = fields.Str()
    external_uid = fields.UUID()

    @post_load
    def make_object(self, data):
        return Tier(**data)


class TiersMixin(BaseModel):
    customer = None  # type: Tier
    tier1 = None  # type: Tier
    tier2 = None  # type: Tier


class TiersMixinSchema(Schema):
    customer = fields.Nested(TierSchema)
    tier1 = fields.Nested(TierSchema)
    tier2 = fields.Nested(TierSchema)

    @post_load
    def make_object(self, data):
        return TiersMixin(**data)
