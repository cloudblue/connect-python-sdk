# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import Schema, fields, post_load

from .base import BaseModel, BaseSchema
from .contact import ContactInfo, ContactInfoSchema


class Tier(BaseModel):
    name = None  # type: str
    contact_info = None  # type: ContactInfo
    external_id = None  # type: str
    external_uid = None  # type: str


class TierSchema(BaseSchema):
    name = fields.Str()
    contact_info = fields.Nested(ContactInfoSchema)
    external_id = fields.Str()
    external_uid = fields.UUID()

    @post_load
    def make_object(self, data):
        return Tier(**data)


class Tiers(BaseModel):
    customer = None  # type: Tier
    tier1 = None  # type: Tier
    tier2 = None  # type: Tier


class TiersSchema(Schema):
    customer = fields.Nested(TierSchema)
    tier1 = fields.Nested(TierSchema)
    tier2 = fields.Nested(TierSchema)

    @post_load
    def make_object(self, data):
        return Tiers(**data)
