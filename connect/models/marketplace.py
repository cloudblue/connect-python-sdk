# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.
import datetime
from typing import Optional, List

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema
from .company import Company, CompanySchema
from .hub import ExtIdHub, ExtIdHubSchema


class MarketplaceSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str()
    active_contracts = fields.Int()
    icon = fields.Str()
    owner = fields.Nested(CompanySchema, only=('id', 'name'))
    hubs = fields.Nested(ExtIdHubSchema, many=True)
    zone = fields.Str()

    @post_load
    def make_object(self, data):
        return Marketplace(**data)


class AgreementStatsSchema(BaseSchema):
    contracts = fields.Int(allow_none=True)
    versions = fields.Int()

    @post_load
    def make_object(self, data):
        return AgreementStatsSchema(**data)


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


class ActivationSchema(BaseSchema):
    link = fields.Str(allow_none=True)
    message = fields.Str()
    date = fields.DateTime(allow_none=True)

    @post_load
    def make_object(self, data):
        return Activation(**data)


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
    enrolled = fields.DateTime(allow_none=True)
    version_created = fields.DateTime()
    activation = fields.Nested(ActivationSchema)
    signee = fields.Nested(CompanySchema, only=('id', 'name'), allow_none=True)

    @post_load
    def make_object(self, data):
        return Contract(**data)


class Marketplace(BaseModel):
    """ An object containing Distribution agreements with exact Hubs, enriched with additional
    information on details about the relation.

    A Marketplace is a way to list Products to specified regions (based on Distribution Agreements)
    and use specific Hubs to provision incoming Fulfillment requests.
    """

    _schema = MarketplaceSchema()

    name = None  # type: str
    """ (str) Marketplace title, unique for an account. """

    description = None  # type: str
    """ (str) Markdown text describing the marketplace. """

    active_contracts = None  # type: int
    """ (int) How many active contracts were signed on the Marketplace. """

    icon = None  # type: str
    """ (str) Image identifying Marketplace object uploaded by user. """

    owner = None  # type: Company
    """ (:py:class:`.Company`) Provider account - the object owner. """

    hubs = None  # type: List[ExtIdHub]
    """ (List[:py:class:`.ExtIdHub`]) List of account-hub relations associated
    with the Marketplace object.
    """

    zone = None  # type: str
    """ (str) Zone where the marketplace is located, there can be following zones:
    AF, NA, OC, AS, EU, SA (It is continents). """


class AgreementStats(BaseModel):
    """ Agreement stats. """

    _schema = AgreementStatsSchema()

    contracts = None  # type: Optional[int]
    """ (int|None) Number of contracts this agreement has. """

    versions = None  # type: int
    """ (int) Number of versions in the agreement. """


class Agreement(BaseModel):
    """ An Agreement object. """

    _schema = AgreementSchema()

    type = None  # type: str
    """ (str) Type of the agreement. One of: distribution, program, service. """

    title = None  # type: str
    """ (str) Title of the agreement. """

    description = None  # type: str
    """ (str) Agreement details (Markdown). """

    created = None  # type: datetime.datetime
    """ (datetime.datetime) Date of creation of the agreement. """

    updated = None  # type: datetime.datetime
    """ (datetime.datetime) Date of the update of the agreement. It can be creation
    of the new version, change of the field, etc. (any change).
    """

    owner = None  # type: Company
    """ (:py:class:`.Company`) Reference to the owner account object. """

    stats = None  # type: Optional[AgreementStats]
    """ (:py:class:`.AgreementStats` | None) Agreement stats. """

    author = None  # type: Optional[Company]
    """ (:py:class:`.Company` | None) Reference to the user who created the version. """

    version = None  # type: int
    """ (int) Chronological number of the version. """

    active = None  # type: bool
    """ (bool) State of the version. """

    link = None  # type: str
    """ (str) Url to the document. """

    version_created = None  # type: datetime.datetime
    """ (datetime.datetime) Date of the creation of the version. """

    version_contracts = None  # type: int
    """ (int) Number of contracts this version has. """

    agreements = None  # type: List[Agreement]
    """ (List[:py:class:`.Agreement`]) Program agreements can have distribution agreements
    associated with them.
    """

    parent = None  # type: Optional[Agreement]
    """ (:py:class:`.Agreement` | None) Reference to the parent program agreement
    (for distribution agreement).
    """

    marketplace = None  # type: Optional[Marketplace]
    """ (:py:class:`.Marketplace` | None) Reference to marketplace object
    (for distribution agreement).
    """


class Activation(BaseModel):
    """ Activation object. """

    _schema = ActivationSchema()

    link = None  # type: Optional[str]
    """ (str|None) Activation link. """

    message = None  # type: str
    """ (str) Activation message. """

    date = None  # type: Optional[datetime.datetime]
    """ (datetime.datetime|None) Activation date. """


class Contract(BaseModel):
    """ Contract object. """

    _schema = ContractSchema()

    name = None  # type: str
    """ (str) Contract name. """

    version = None  # type: int
    """ (int) Version of the contract (same as associated agreement version). """

    type = None  # type: str
    """ (str) Type of the contract (same as agreement type). One of:
    distribution, program, service.
    """

    status = None  # type: str
    """ (str) Contract Status. One of: enrolling, pending, active, terminated, rejected """

    agreement = None  # type: Agreement
    """ (:py:class:`.Agreement`) Reference object to the agreement. """

    marketplace = None  # type: Optional[Marketplace]
    """ (:py:class:`.Marketplace` | None) Reference object to the agreement marketplace. """

    owner = None  # type: Optional[Company]
    """ (:py:class:`.Company` | None) Reference object to the owner company. """

    creator = None  # type: Company
    """ (:py:class:`.Company`) Reference object to the creator company. """

    created = None  # type: datetime.datetime
    """ (datetime.datetime) Contract creation date. """

    updated = None  # type: datetime.datetime
    """ (datetime.datetime) Date of contract status update. """

    enrolled = None  # type: Optional[datetime.datetime]
    """ (datetime.datetime|None) Date when contract was enrolled. """

    version_created = None  # type: datetime.datetime
    """ (datetime.datetime) Contract version creation date. """

    activation = None  # type: Activation
    """ (:py:class:`.Activation`) Activation information. """

    signee = None  # type: Optional[Company]
    """ (:py:class:`.Company` | None) Reference object to the user of the owner company,
    who signed the contract.
    """
