# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import List, Optional

from .base import BaseModel
from .connection import Connection
from .parameters import Param
from .product import Item, Product
from .tier_config import TierAccounts
from connect.models.schemas import AssetSchema


class Asset(BaseModel):
    """ Represents a saleable item that can be provided/distributed in terms of one purchase.

    These assets can be requested using :py:class:`connect.resource.FulfillmentAutomation`
    resource.

    An asset is characterized by the following:

    - Every asset reflects some purchase (somebody purchases either a service or a good).
    - Purchase action can be reverted (canceled) or terminated when terms of purchase are expired,
      see full state diagram on FIG.5
    - Asset can be subscription-based (when customer pay for usage in some time terms) or
      one-time based.
    - Matter of asset is defined as list of purchased items with purchased quantities
      (asset items).
    - Item in asset may be either reservation-based, when customer decides how many items of SKU
      to be purchased or Pay-Per-User based when actual use of the SKU defines quantity for
      asset item.
    - Asset may be modified using change requests: either set of items may be changed or quantities
      of reservation-based items may be changed.
    - Some assets can be put into suspend state, when service is not actually provided
      and no charges happened.
    - Assets also may be parametrized by one or more parameters which are differentiate
      one asset from another.
    """

    _schema = AssetSchema()

    status = None  # type: str
    """ Assets may have one of the following statuses:

    - new: First purchase requested.
    - processing: Until first purchase request is either completed or rejected.
    - active: After the first purchase request is completed.
      NOTE: Asset stays active regardless of any other requests except cancel.
    - rejected: Asset becomes rejected once the first purchase request is rejected.
    - terminated: Asset becomes terminated once the 'cancel' request type is fulfilled.
    - suspended: Asset becomes suspended once 'suspend' request type is fulfilled.
    """

    external_id = None  # type: str
    """ (str) Identification for asset object on eCommerce. """

    external_uid = None  # type: Optional[str]
    """ (str|None) Id of asset in eCommerce system """

    product = None  # type: Product
    """ (:py:class:`.Product`) Product object reference. """

    connection = None  # type: Connection
    """ (:py:class:`.Connection`) Connection object. """

    items = None  # type: List[Item]
    """ (List[:py:class:`.Item`]) List of asset product items. """

    params = None  # type: List[Param]
    """ (List[:py:class:`.Param`]) List of product parameter objects. """

    tiers = None  # type: TierAccounts
    """ (:py:class:`.TierAccounts`) Supply chain accounts. """

    def get_param_by_id(self, id_):
        """ Get a parameter of the asset.

        :param str id_: Id of the the parameter to get.
        :return: The parameter with the given id, or ``None`` if it was not found.
        :rtype: :py:class:`.Param` | None
        """
        try:
            return list(filter(lambda param: param.id == id_, self.params))[0]
        except IndexError:
            return None

    def get_item_by_mpn(self, mpn):
        """ Get an item of the asset.

        :param str mpn: MPN of the item to get.
        :return: The item with the given MPN, or ``None`` if it was not found.
        :rtype: :py:class:`.Item` | None
        """
        try:
            return list(filter(lambda item: item.mpn == mpn, self.items))[0]
        except IndexError:
            return None
