# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from marshmallow import fields, post_load
from typing import Optional, List

from .base import BaseModel, BaseSchema
from .company import User, UserSchema
from .connection import Connection, ConnectionSchema
from .contact import ContactInfo, ContactInfoSchema
from .event import EventsSchema, Events
from .marketplace import Activation, ActivationSchema
from .parameters import Param, ParamSchema
from .product import Product, ProductSchema


class Account(BaseModel):
    name = None  # type: str
    external_id = None  # type: str
    external_uid = None  # type: str
    contact_info = None  # type: ContactInfo


class AccountSchema(BaseSchema):
    name = fields.Str()
    external_id = fields.Str()
    external_uid = fields.Str()
    contact_info = fields.Nested(ContactInfoSchema)

    @post_load
    def make_object(self, data):
        return Account(**data)


class Template(BaseModel):
    representation = None  # type: str


class TemplateSchema(BaseSchema):
    representation = fields.Str()

    @post_load
    def make_object(self, data):
        return Template(**data)


class TierConfig(BaseModel):
    name = None  # type: str
    account = None  # type: Account
    product = None  # type: Product
    tier_level = None  # type: int
    connection = None  # type: Connection
    events = None  # type: Optional[Events]
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


class TierConfigSchema(BaseSchema):
    name = fields.Str()
    account = fields.Nested(AccountSchema)
    product = fields.Nested(ProductSchema)
    tier_level = fields.Int()
    connection = fields.Nested(ConnectionSchema)
    events = fields.Nested(EventsSchema, allow_none=True)
    params = fields.Nested(ParamSchema, many=True)
    template = fields.Nested(TemplateSchema)

    # Undocumented fields (they appear in PHP SDK)
    open_request = fields.Nested(BaseSchema)

    @post_load
    def make_object(self, data):
        return TierConfig(**data)


class TierConfigRequest(BaseModel):
    type = None  # type: str
    status = None  # type: str
    configuration = None  # type: TierConfig
    events = None  # type: Optional[Events]
    params = None  # type: List[Param]
    assignee = None  # type: Optional[User]
    template = None  # type: Optional[Template]
    reason = None  # type: Optional[str]
    activation = None  # type: Optional[Activation]
    notes = None  # type: Optional[str]

    def get_param_by_id(self, id_):
        # type: (str) -> Optional[Param]
        try:
            return list(filter(lambda param: param.id == id_, self.params))[0]
        except IndexError:
            return None


class TierConfigRequestSchema(BaseSchema):
    type = fields.Str()
    status = fields.Str()
    configuration = fields.Nested(TierConfigSchema)
    events = fields.Nested(EventsSchema, allow_none=True)
    params = fields.Nested(ParamSchema, many=True)
    assignee = fields.Nested(UserSchema, allow_none=True)
    template = fields.Nested(TemplateSchema, allow_none=True)
    reason = fields.Str(allow_none=True)
    activation = fields.Nested(ActivationSchema, allow_none=True)
    notes = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        return TierConfigRequest(**data)
