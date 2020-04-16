# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .company import Company
from .contract import Contract
from .product import Product
from .schemas import UsageListingSchema


class UsageListing(BaseModel):
    """ Usage Listing Object. """

    _schema = UsageListingSchema()

    status = None  # type: str
    """ (str) Status. """

    contract = None  # type: Contract
    """ (:py:class:`.Contract`) Contract Object. """

    product = None  # type: Product
    """ (:py:class:`.Product`) Product Object. """

    created = None  # type: str
    """ (str) Creation time. """

    # Undocumented fields (they appear in PHP SDK)

    vendor = None  # type: Company
    """ (:py:class:`.Company`) Vendor Object. """

    provider = None  # type: Company
    """ (:py:class:`.Company`) Provider Object. """
