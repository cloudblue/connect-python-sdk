# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from marshmallow import fields, post_load
from typing import Optional, List

from connect.models import Param, ParamSchema
from connect.models.base import BaseModel, BaseSchema
from connect.models.company import Company, CompanySchema
from connect.models.connection import Connection, ConnectionSchema
from connect.models.contact import ContactInfo, ContactInfoSchema
from connect.models.product import Product, ProductSchema


class Account(BaseModel):
    name = None  # type: str
    external_id = None  # type: str
    external_uid = None  # type: str
    contact_info = None  # type: ContactInfo


class EventInfo(BaseModel):
    at = None  # type: str
    by = None  # type: Company


class Events(BaseModel):
    created = None  # type: EventInfo
    inquired = None  # type: EventInfo
    pended = None  # type: EventInfo
    validated = None  # type: EventInfo
    updated = None  # type: EventInfo


class Template(BaseModel):
    representation = None  # type: str


class TierConfig(BaseModel):
    name = None  # type: str
    account = None  # type: Account
    product = None  # type: Product
    tier_level = None  # type: int
    connection = None  # type: Connection
    events = None  # type: Events
    params = None  # type: List[Param]
    template = None  # type: Template

    # Undocumented fields (they appear in PHP SDK)
    open_request = None  # type: BaseModel

    def get_param_by_id(self, id_):
        # type: (str) -> Optional[Param]
        try:
            return list(filter(lambda param: param.id == id_, self.params))[0]
        except IndexError:
            return None


class Activation(BaseModel):
    link = None  # type: str


class TierConfigRequest(BaseModel):
    type = None  # type: str
    status = None  # type: str
    configuration = None  # type: TierConfig
    events = None  # type: Events
    params = None  # type: List[Param]
    assignee = None  # type: Company
    template = None  # type: Template
    activation = None  # type: Activation

    def get_param_by_id(self, id_):
        # type: (str) -> Optional[Param]
        try:
            return list(filter(lambda param: param.id == id_, self.params))[0]
        except IndexError:
            return None


class AccountSchema(BaseSchema):
    name = fields.Str()
    external_id = fields.Str()
    external_uid = fields.Str()
    contact_info = fields.Nested(ContactInfoSchema)

    @post_load
    def make_object(self, data):
        return Account(**data)


class EventInfoSchema(BaseSchema):
    at = fields.Str()
    by = fields.Nested(CompanySchema)

    @post_load
    def make_object(self, data):
        return EventInfo(**data)


class EventsSchema(BaseSchema):
    created = fields.Nested(EventInfoSchema)
    inquired = fields.Nested(EventInfoSchema, required=False)
    pended = fields.Nested(EventInfoSchema, required=False)
    validated = fields.Nested(EventInfoSchema, required=False)
    updated = fields.Nested(EventInfoSchema, required=False)

    @post_load
    def make_object(self, data):
        return Events(**data)


class TemplateSchema(BaseSchema):
    representation = fields.Str()

    @post_load
    def make_object(self, data):
        return Template(**data)


class TierConfigSchema(BaseSchema):
    name = fields.Str()
    account = fields.Nested(AccountSchema)
    product = fields.Nested(ProductSchema)
    tier_level = fields.Int()
    connection = fields.Nested(ConnectionSchema)
    events = fields.Nested(EventsSchema)
    params = fields.List(fields.Nested(ParamSchema))
    template = fields.Nested(TemplateSchema)

    # Undocumented fields (they appear in PHP SDK)
    open_request = fields.Nested(BaseSchema)

    @post_load
    def make_object(self, data):
        return TierConfig(**data)


class ActivationSchema(BaseSchema):
    link = fields.Str()

    @post_load
    def make_object(self, data):
        return Activation(**data)


class TierConfigRequestSchema(BaseSchema):
    type = fields.Str()
    status = fields.Str()
    configuration = fields.Nested(TierConfigSchema)
    events = fields.Nested(EventsSchema)
    params = fields.List(fields.Nested(ParamSchema))
    assignee = fields.Nested(CompanySchema)
    template = fields.Nested(TemplateSchema)
    activation = fields.Nested(ActivationSchema)

    @post_load
    def make_object(self, data):
        return TierConfigRequest(**data)
