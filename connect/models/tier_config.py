# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import Optional, List

from .base import BaseModel
from .company import User
from .connection import Connection
from .contact import ContactInfo
from .event import Events
from .marketplace import Activation
from .parameters import Param
from .product import Product
from connect.models.schemas import TemplateSchema, TierAccountSchema, \
    TierAccountsSchema, TierConfigSchema, TierConfigRequestSchema


class TierAccount(BaseModel):
    """ Tier account. """

    _schema = TierAccountSchema()

    name = None  # type: str
    """ (str) Tier name. """

    contact_info = None  # type: ContactInfo
    """ (:py:class:`.ContactInfo`) Tier Contact Object. """

    external_id = None  # type: Optional[str]
    """ (str|None) Only in case of filtering by this field. """

    external_uid = None  # type: Optional[str]
    """ (str|None) Only in case of filtering by this field. """


class TierAccounts(BaseModel):
    """ TierAccounts object. """

    _schema = TierAccountsSchema()

    customer = None  # type: TierAccount
    """ (:py:class:`.TierAccount`) Customer Level TierAccount Object. """

    tier1 = None  # type: TierAccount
    """ (:py:class:`.TierAccount`) Level 1 TierAccount Object. """

    tier2 = None  # type: TierAccount
    """ (:py:class:`.TierAccount`) Level 2 TierAccount Object. """


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

    account = None  # type: TierAccount
    """ (:py:class:`.TierAccount`) Full tier account representation
    (same as in :py:class:`.Asset`).
    """

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

    @classmethod
    def get(cls, account_id, product_id, config=None):
        """
        Gets the specified tier config data. For example, to get Tier 1 configuration data
        for one request we can do: ::

            TierConfig.get(request.asset.tiers.tier1.id, request.asset.product.id)

        :param str account_id: Account Id of the requested Tier Config (id with TA prefix).
        :param str product_id: Id of the product.
        :param Config config: Config to use, or ``None`` to use environment config (default).
        :return: The requested Tier Config, or ``None`` if it was not found.
        :rtype: Optional[TierConfig]
        """
        from connect.resources.base import ApiClient

        response, _ = ApiClient(config, base_path='tier/config-requests').get(
            params={
                'status': 'approved',
                'configuration__product__id': product_id,
                'configuration__account__id': account_id,
            }
        )
        objects = TierConfigRequest.deserialize(response)

        if isinstance(objects, list) and len(objects) > 0:
            return objects[0].configuration
        else:
            return None

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

    assignee = None  # type: Optional[User]
    """ (:py:class:`.User` | None) TCR environment. One of: test, prod, preview. """

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
