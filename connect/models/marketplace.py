# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema
from .company import Company, CompanySchema
from .hub import Hubs, HubsSchema


class Marketplace(BaseModel):
    name = None  # type: str
    zone = None  # type: str
    description = None  # type: str
    active_contract = None  # type: int
    icon = None  # type: str
    owner = None  # type: Company
    hubs = None  # type: Hubs


class MarketplaceSchema(BaseSchema):
    name = fields.Str()
    zone = fields.Str()
    description = fields.Str()
    active_contract = fields.Int()
    icon = fields.Str()
    owner = fields.Nested(CompanySchema, only=('id', 'name'))
    hubs = fields.List(fields.Nested(HubsSchema, only=('id', 'name')))

    @post_load
    def make_object(self, data):
        return Marketplace(**data)


class Agreement(BaseModel):
    type = None  # type: str
    title = None  # type: str
    description = None  # type: str
    created = None  # type: str
    updated = None  # type: str
    owner = None  # type: Company
    stats = None  # type: dict
    active = None  # type: bool
    version = None  # type: int
    link = None  # type: str
    version_created = None  # type: str
    version_contracts = None  # type: int


class AgreementSchema(BaseSchema):
    type = fields.Str()
    title = fields.Str()
    description = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    owner = fields.Nested(CompanySchema, only=('id', 'name'))
    stats = fields.Dict()
    active = fields.Bool()
    version = fields.Int()
    link = fields.Str()
    version_created = fields.DateTime()
    version_contracts = fields.Int()

    @post_load
    def make_object(self, data):
        return Agreement(**data)


class Contract(BaseModel):
    name = None  # type: str
    status = None  # type: str
    version = None  # type: int
    type = None  # type: str
    agreement = None  # type: Agreement
    marketplace = None  # type: Marketplace
    owner = None  # type: Company
    creater = None  # type: Company
    created = None  # type: str
    updated = None  # type: str
    enrolled = None  # type: str
    version_created = None  # type: str
    activation = None  # type: dict
    signee = None  # type: Company


class ContractSchema(BaseSchema):
    name = fields.Str()
    status = fields.Str()
    version = fields.Int()
    type = fields.Str()
    agreement = fields.Nested(AgreementSchema, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'))
    owner = fields.Nested(CompanySchema, only=('id', 'name'))
    creater = fields.Nested(CompanySchema, only=('id', 'name'))
    created = fields.DateTime()
    updated = fields.DateTime()
    enrolled = fields.Str()
    version_created = fields.DateTime()
    activation = fields.Dict()
    signee = fields.Nested(CompanySchema, only=('id', 'name'))

    @post_load
    def make_object(self, data):
        return Contract(**data)
