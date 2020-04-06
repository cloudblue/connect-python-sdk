# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import Optional, List

from .activation import Activation
from .base import BaseModel
from .contract import Contract
from .events import Events
from .marketplace import Marketplace
from .param import Param
from .product import Product
from .template import Template
from .tier_account import TierAccount
from .tier_accounts import TierAccounts
from .tier_config import TierConfig
from .user import User
from .schemas import TierConfigRequestSchema


class TierConfigRequest(BaseModel):
    _schema = TierConfigRequestSchema()

    type = None  # type: str
    """ (str) TCR type. One of: setup, update. """

    status = None  # type: str
    """ (str) TCR current status. One of: tiers_setup, pending, inquiring, approved, failed. """

    configuration = None  # type: TierConfig
    """ (:py:class:`.TierConfig`) Full representation of TierConfig Object. """

    parent_configuration = None  # type: Optional[TierConfig]
    """ (:py:class:`.TierConfig` | None) Full representation of parent TierConfig. """

    account = None  # type: TierAccount
    """ (:py:class:`.TierAccount`) Reference object to TierAccount. """

    product = None  # type: Product
    """ (:py:class:`.Product`) Reference object to product (application). """

    tier_level = None  # type: int
    """ (int) Tier level for product from customer perspective (1 or 2). """

    params = None  # type: List[Param]
    """ (List[:py:class:`.Param`]) List of parameter data objects as in Asset Object.
    Params can be modified only in Pending state.
    """

    environment = None  # type: str
    """ (str) TCR environment (test, prod or preview) """

    assignee = None  # type: Optional[User]
    """ (:py:class:`.User` | None) User assigned to this TCR. """

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

    events = None  # type: Optional[Events]
    """ (:py:class:`.Events` | None) Tier Config request Events. """

    # Undocumented fields (they appear in PHP SDK)

    tiers = None  # type: Optional[TierAccounts]
    """ (:py:class:`.TierAccounts` | None) TierConfig tier accounts. """

    marketplace = None  # type: Optional[Marketplace]
    """ (:py:class:`.Marketplace` | None) TierConfig marketplace. """

    contract = None  # type: Optional[Contract]
    """ (:py:class:`.Contract` | None) TierConfig contract. """

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
