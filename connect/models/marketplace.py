# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import fields, post_load
from typing import Optional, List

from .base import BaseModel, BaseSchema
from .company import Company, CompanySchema
from .hub import Hubs, HubsSchema


class Marketplace(BaseModel):
    name = None  # type: str
    description = None  # type: str
    active_contract = None  # type: int
    icon = None  # type: str
    owner = None  # type: Company
    hubs = None  # type: List[Hubs]
    zone = None  # type: str


class MarketplaceSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str()
    active_contract = fields.Int()
    icon = fields.Str()
    owner = fields.Nested(CompanySchema, only=('id', 'name'))
    hubs = fields.Nested(HubsSchema, many=True)
    zone = fields.Str()

    @post_load
    def make_object(self, data):
        return Marketplace(**data)


class AgreementStats(BaseModel):
    contracts = None  # type: Optional[int]
    versions = None  # type: int


class AgreementStatsSchema(BaseSchema):
    contracts = fields.Int(allow_none=True)
    versions = fields.Int()

    @post_load
    def make_object(self, data):
        return AgreementStatsSchema(**data)


class Agreement(BaseModel):
    type = None  # type: str
    title = None  # type: str
    description = None  # type: str
    created = None  # type: str
    updated = None  # type: str
    owner = None  # type: Company
    stats = None  # type: Optional[AgreementStats]
    author = None  # type: Optional[Company]
    version = None  # type: int
    active = None  # type: bool
    link = None  # type: str
    version_created = None  # type: str
    version_contracts = None  # type: int
    agreements = None  # type: List[Agreement]
    parent = None  # type: Optional[Agreement]
    marketplace = None  # type: Optional[Marketplace]


class AgreementSchema(BaseSchema):
    type = fields.Str()
    title = fields.Str()
    description = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    owner = fields.Nested(CompanySchema)
    stats = fields.Nested(AgreementStatsSchema, allow_none=True)
    author = fields.Nested(CompanySchema, allow_none=True)
    version = fields.Int()
    active = fields.Bool()
    link = fields.Str()
    version_created = fields.DateTime()
    version_contracts = fields.Int()
    agreements = fields.Nested('AgreementSchema', many=True)
    parent = fields.Nested('AgreementSchema', only=('id', 'name'), allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'), allow_none=True)

    @post_load
    def make_object(self, data):
        return Agreement(**data)


class Activation(BaseModel):
    link = None  # type: Optional[str]
    message = None  # type: str
    date = None  # type: Optional[str]


class ActivationSchema(BaseSchema):
    link = fields.Str(allow_none=True)
    message = fields.Str()
    date = fields.DateTime(allow_none=True)

    @post_load
    def make_object(self, data):
        return Activation(**data)


class Contract(BaseModel):
    name = None  # type: str
    version = None  # type: int
    type = None  # type: str
    status = None  # type: str
    agreement = None  # type: Agreement
    marketplace = None  # type: Optional[Marketplace]
    owner = None  # type: Optional[Company]
    creator = None  # type: Company
    created = None  # type: str
    updated = None  # type: str
    enrolled = None  # type: Optional[str]
    version_created = None  # type: str
    activation = None  # type: Activation
    signee = None  # type: Optional[Company]


class ContractSchema(BaseSchema):
    name = fields.Str()
    version = fields.Int()
    type = fields.Str()
    status = fields.Str()
    agreement = fields.Nested(AgreementSchema, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'), allow_none=True)
    owner = fields.Nested(CompanySchema, only=('id', 'name'), allow_none=True)
    creator = fields.Nested(CompanySchema, only=('id', 'name'))
    created = fields.DateTime()
    updated = fields.DateTime()
    enrolled = fields.Str(allow_none=True)
    version_created = fields.DateTime()
    activation = fields.Nested(ActivationSchema)
    signee = fields.Nested(CompanySchema, only=('id', 'name'), allow_none=True)

    @post_load
    def make_object(self, data):
        return Contract(**data)
