# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import Schema, fields, post_load
from typing import Optional

from connect.models.company import Company, CompanySchema
from connect.models.event import Events, EventsSchema
from .base import BaseModel, BaseSchema


class HubInstance(BaseModel):
    type = None  # type: str


class HubInstanceSchema(BaseSchema):
    type = fields.Str()

    @post_load
    def make_object(self, data):
        return HubInstance(**data)


class HubStats(BaseModel):
    connections = None  # type: int
    marketplaces = None  # type: int


class HubStatsSchema(BaseSchema):
    connections = fields.Int()
    marketplaces = fields.Int()

    @post_load
    def make_object(self, data):
        return HubStats(**data)


class Hub(BaseModel):
    name = None  # type: str
    company = None  # type: Company
    description = None  # type: Optional[str]
    instance = None  # type: HubInstance
    events = None  # type: Events
    stats = None  # type: HubStats


class HubSchema(BaseSchema):
    name = fields.Str()
    company = fields.Nested(CompanySchema)
    description = fields.Str(allow_none=True)
    instance = fields.Nested(HubInstanceSchema)
    events = fields.Nested(EventsSchema)
    stats = fields.Nested(HubStatsSchema)

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
