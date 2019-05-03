# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import Schema, fields, post_load
from typing import Optional

from .base import BaseModel, BaseSchema
from .company import Company, CompanySchema
from .event import Events, EventsSchema


class HubInstance(BaseModel):
    """ An instance of a hub. """

    type = None  # type: str
    """ (str) E-Commerce system type. """


class HubInstanceSchema(BaseSchema):
    type = fields.Str()

    @post_load
    def make_object(self, data):
        return HubInstance(**data)


class HubStats(BaseModel):
    """ Hub stats. """

    connections = None  # type: int
    """ (int) Number of connections active for this Hub. """

    marketplaces = None  # type: int
    """ (int) Number of marketplaces for this Hub. """


class HubStatsSchema(BaseSchema):
    connections = fields.Int()
    marketplaces = fields.Int()

    @post_load
    def make_object(self, data):
        return HubStats(**data)


class Hub(BaseModel):
    """ A Hub. """

    name = None  # type: str
    """ (str) Hub name. """

    company = None  # type: Company
    """ (:py:class:`.Company`) Reference to the company the hub belongs to. """

    description = None  # type: Optional[str]
    """ (str|None) Hub description (Markdown text). """

    instance = None  # type: HubInstance
    """ (:py:class:`.HubInstance`) Hub instance. """

    events = None  # type: Events
    """ (:py:class:`.Events`) Events occurred on Hub. """

    stats = None  # type: HubStats
    """ (:py:class:`.HubStats`) Hub stats. """


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


class ExtIdHub(BaseModel):
    """ Associates a :py:class:`.Hub` with an external id. """

    hub = None  # type: Hub
    """ (:py:class:`.Hub`) Hub. """

    external_id = None  # type: str
    """ (str) External id. """


class ExtIdHubSchema(Schema):
    hub = fields.Nested(HubSchema, only=('id', 'name'))
    external_id = fields.Str()

    @post_load
    def make_object(self, data):
        return ExtIdHub(**data)
