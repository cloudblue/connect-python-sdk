# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import List

from .base import BaseModel
from .company import Company
from .country import Country
from .ext_id_hub import ExtIdHub
from .schemas import MarketplaceSchema


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

    countries = None  # type: List[Country]
    """ List[:py:class:`.Country`] 	List of country objects associated with marketplace. """

    sourcing = None  # type: bool
    """ (bool) Is marketplace available for sourcing. """
