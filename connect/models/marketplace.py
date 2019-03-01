# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema
from .company import CompanySchema
from .hub import HubsSchemaMixin


class Marketplace(BaseModel):
    pass


class MarketplaceSchema(BaseSchema):
    name = fields.Str()
    zone = fields.Str()
    description = fields.Str()
    active_contract = fields.Int()
    icon = fields.Str()
    owner = fields.Nested(CompanySchema, only=('id', 'name'))
    hubs = fields.List(fields.Nested(HubsSchemaMixin, only=('id', 'name')))

    @post_load
    def make_object(self, data):
        return Marketplace(**data)


class Agreement(BaseModel):
    pass


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
    pass


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
