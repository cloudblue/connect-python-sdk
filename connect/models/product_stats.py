# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .product_stats_info import ProductStatsInfo
from .schemas import ProductStatsSchema


class ProductStats(BaseModel):
    """ Statistics of product use. """

    _schema = ProductStatsSchema()

    listing = None  # type: int
    """ (int) Number of listings (direct use of product by provider). """

    agreements = None  # type: ProductStatsInfo
    """ (:py:class:`.ProductStatsInfo`) Agreements related to the product. """

    contracts = None  # type: ProductStatsInfo
    """ (:py:class:`.ProductStatsInfo`) Contracts related to the product. """
