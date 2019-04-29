# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from marshmallow import fields, post_load
from typing import Optional

from connect.models.base import BaseModel, BaseSchema
from connect.models.company import CompanySchema, Company


class EventInfo(BaseModel):
    at = None  # type: Optional[str]
    by = None  # type: Optional[Company]


class EventInfoSchema(BaseSchema):
    at = fields.Str(allow_none=True)
    by = fields.Nested(CompanySchema, allow_none=True)

    @post_load
    def make_object(self, data):
        return EventInfo(**data)


class Events(BaseModel):
    created = None  # type: EventInfo
    inquired = None  # type: EventInfo
    pended = None  # type: EventInfo
    validated = None  # type: EventInfo
    updated = None  # type: EventInfo


class EventsSchema(BaseSchema):
    created = fields.Nested(EventInfoSchema)
    inquired = fields.Nested(EventInfoSchema)
    pended = fields.Nested(EventInfoSchema)
    validated = fields.Nested(EventInfoSchema)
    updated = fields.Nested(EventInfoSchema)

    @post_load
    def make_object(self, data):
        return Events(**data)
