# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import Optional, List

from .base import BaseModel
from .configuration import Configuration
from .connection import Connection
from .contract import Contract
from .events import Events
from .marketplace import Marketplace
from .param import Param
from .product import Product
from .template import Template
from .tier_account import TierAccount
from .schemas import TierConfigSchema


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

    params = None  # type: List[Param]
    """ (List[:py:class:`.Param`]) List of TC parameter data objects as in Asset Object
    extended with unfilled parameters from product.
    """

    connection = None  # type: Connection
    """ (:py:class:`.Connection`) Reference to Connection Object. """

    open_request = None  # type: Optional[BaseModel]
    """ (:py:class:`.BaseModel` | None) Reference to TCR. """

    template = None  # type: Template
    """ (:py:class:`.Template`) Template Object.  """

    contract = None  # type: Contract
    """ (:py:class:`.Contract`) Contract Object reference. """

    marketplace = None  # type: Marketplace
    """ (:py:class:`.Marketplace`) Marketplace Object reference. """

    configuration = None  # type: Configuration
    """ (:py:class:`.Configuration`) List of Product and Marketplace Configuration Phase Parameter
    Context-Bound Object.
    """

    events = None  # type: Optional[Events]
    """ (:py:class:`.Events` | None) Tier Config events. """

    # Undocumented fields (they appear in PHP SDK)

    status = None  # type: str
    """ (str) TierConfig status. """

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
        from .tier_config_request import TierConfigRequest
        from connect.resources.base import ApiClient

        response, _ = ApiClient(config, base_path='tier/config-requests').get(
            params={
                'status': 'approved',
                'configuration.product.id': product_id,
                'configuration.account.id': account_id,
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
