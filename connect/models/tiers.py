# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import Schema, fields, post_load

from .base import BaseModel, BaseSchema
from .contact import ContactInfo, ContactInfoSchema


class TierSchema(BaseSchema):
    name = fields.Str()
    contact_info = fields.Nested(ContactInfoSchema)
    external_id = fields.Str()
    external_uid = fields.Str()

    @post_load
    def make_object(self, data):
        return Tier(**data)


class TiersSchema(Schema):
    customer = fields.Nested(TierSchema)
    tier1 = fields.Nested(TierSchema)
    tier2 = fields.Nested(TierSchema)

    @post_load
    def make_object(self, data):
        return Tiers(**data)


class Tier(BaseModel):
    """ Tier Object. """

    _schema = TierSchema()

    name = None  # type: str
    """ (str) Tier name. """

    contact_info = None  # type: ContactInfo
    """ (:py:class:`.ContactInfo`) Tier Contact Object. """

    external_id = None  # type: str
    """ (str) External id. """

    external_uid = None  # type: str
    """ (str) External uid. """


class Tiers(BaseModel):
    """ Tiers object. """

    _schema = TiersSchema()

    customer = None  # type: Tier
    """ (:py:class:`.Tier`) Customer Level Tier Object. """

    tier1 = None  # type: Tier
    """ (:py:class:`.Tier`) Level 1 Tier Object. """

    tier2 = None  # type: Tier
    """ (:py:class:`.Tier`) Level 2 Tier Object. """
