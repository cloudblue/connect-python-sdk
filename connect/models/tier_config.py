# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import fields, post_load
from typing import Optional, List

from .base import BaseModel, BaseSchema
from .company import Company, CompanySchema
from .connection import Connection, ConnectionSchema
from .contact import ContactInfo, ContactInfoSchema
from .event import EventsSchema, Events
from .marketplace import Activation, ActivationSchema
from .parameters import Param, ParamSchema
from .product import Product, ProductSchema


class AccountSchema(BaseSchema):
    name = fields.Str()
    external_id = fields.Str(allow_none=True)
    external_uid = fields.Str(allow_none=True)
    contact_info = fields.Nested(ContactInfoSchema)

    @post_load
    def make_object(self, data):
        return Account(**data)


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
    events = fields.Nested(EventsSchema, allow_none=True)
    params = fields.Nested(ParamSchema, many=True)
    template = fields.Nested(TemplateSchema)
    open_request = fields.Nested(BaseSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        return TierConfig(**data)


class TierConfigRequestSchema(BaseSchema):
    type = fields.Str()
    status = fields.Str()
    configuration = fields.Nested(TierConfigSchema)
    events = fields.Nested(EventsSchema, allow_none=True)
    params = fields.Nested(ParamSchema, many=True)
    assignee = fields.Nested(CompanySchema, allow_none=True)
    template = fields.Nested(TemplateSchema, allow_none=True)
    reason = fields.Str(allow_none=True)
    activation = fields.Nested(ActivationSchema, allow_none=True)
    notes = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        return TierConfigRequest(**data)


class Account(BaseModel):
    """ Tier account. """

    _schema = AccountSchema()

    name = None  # type: str
    """ (str) Account name. """

    external_id = None  # type: Optional[str]
    """ (str|None) Only in case of filtering by this field. """
    external_uid = None  # type: Optional[str]
    """ (str|None) Only in case of filtering by this field. """

    contact_info = None  # type: ContactInfo
    """ (:py:class:`.ContactInfo`) Contact. """


class Template(BaseModel):
    """ Tier Template """

    _schema = TemplateSchema()

    representation = None  # type: str
    """ (str) Template representation. """


class TierConfig(BaseModel):
    """ Full representation of Tier object. """

    _schema = TierConfigSchema()

    name = None  # type: str
    """ (str) Tier configuration of account.name. """

    account = None  # type: Account
    """ (:py:class:`.Account`) Full tier account representation (same as in Asset). """

    product = None  # type: Product
    """ (:py:class:`.Product`) Reference object to product (application). """

    tier_level = None  # type: int
    """ (int) Tier level for product from customer perspective. """

    connection = None  # type: Connection
    """ (:py:class:`.Connection`) Reference to Connection Object. """

    events = None  # type: Optional[Events]
    """ (:py:class:`.Events` | None) Tier Config events. """

    params = None  # type: List[Param]
    """ (List[:py:class:`.Param`]) List of TC parameter data objects as in Asset Object
    extended with unfilled parameters from product.
    """

    template = None  # type: Template
    """ (:py:class:`.Template`) Template Object.  """

    open_request = None  # type: Optional[BaseModel]
    """ (:py:class:`.BaseModel` | None) Reference to TCR. """

    def get_param_by_id(self, id_):
        """ Get a Tier Config parameter.

        :param str id_: Parameter id.
        :return: The requested parameter, or ``None`` if it was not found.
        :rtype: Param
        """
        try:
            return list(filter(lambda param: param.id == id_, self.params))[0]
        except IndexError:
            return None


class TierConfigRequest(BaseModel):
    _schema = TierConfigRequestSchema()

    type = None  # type: str
    """ (str) TCR type. One of: setup, update. """

    status = None  # type: str
    """ (str) TCR current status. One of: tiers_setup, pending, inquiring, approved, failed. """

    configuration = None  # type: TierConfig
    """ (:py:class:`.TierConfig`) Full representation of Tier Configuration Object. """

    events = None  # type: Optional[Events]
    """ (:py:class:`.Events` | None) Tier Config request Events. """

    params = None  # type: List[Param]
    """ (List[:py:class:`.Param`]) List of parameter data objects as in Asset Object.
    Params can be modified only in Pending state.
    """

    assignee = None  # type: Optional[Company]
    """ (:py:class:`.Company` | None) TCR environment. One of: test, prod, preview. """

    template = None  # type: Optional[Template]
    """ (:py:class:`.Template` | None) Template Object. This is filled only if TCR is approved. """

    reason = None  # type: Optional[str]
    """ (str|None) Failing reason. This is filled only if TCR is failed. """

    activation = None  # type: Optional[Activation]
    """ (:py:class:`.Activation` | None) Activation object. This is created only if TCR
    has ordering parameters and seen in inquiring state of the TCR.
    """

    notes = None  # type: Optional[str]
    """ (str) TCR pending notes. Notes can be modified only in Pending state. """

    def get_param_by_id(self, id_):
        """ Get a Tier Config Request parameter.

        :param str id_: Parameter id.
        :return: The requested parameter, or ``None`` if it was not found.
        :rtype: Param
        """
        try:
            return list(filter(lambda param: param.id == id_, self.params))[0]
        except IndexError:
            return None
