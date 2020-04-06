# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from copy import copy
import datetime
from typing import Optional

from .base import BaseModel
from .company import Company
from .customer_ui_settings import CustomerUiSettings
from .product_category import ProductCategory
from .product_configuration import ProductConfiguration
from .product_configuration_parameter import ProductConfigurationParameter
from .product_stats import ProductStats
from .schemas import ProductSchema
from .template import Template
from connect.config import Config
from connect.resources.base import ApiClient
from connect.rql import Query


class Product(BaseModel):
    """ Represents basic marketing information about salable items, parameters, configurations,
    latest published version and connections.

    It contains basic product information like name, description and logo, along with the latest
    published version details. So in a single point we can say a single product object always
    represent the latest published version of that product.
    """

    _schema = ProductSchema()

    name = None  # type: str
    """ (str) Product name. """

    icon = None  # type: str
    """ (str) Product icon URI. """

    short_description = None  # type: str
    """ (str) Short description of product. """

    detailed_description = None  # type: str
    """ (str) Detailed description of product. """

    version = None  # type: int
    """ (int) Version of product. """

    published_at = None  # type: Optional[datetime.datetime]
    """ (datetime.datetime) Date of publishing. """

    configurations = None  # type: ProductConfiguration
    """ (:py:class:`.ProductConfiguration`) Product configuration. """

    customer_ui_settings = None  # type: CustomerUiSettings
    """ (:py:class:`.CustomerUiSettings`) Customer Ui Settings. """

    category = None  # type: Optional[ProductCategory]
    """ (:py:class:`.ProductCategory` | None) Reference to ProductCategory Object. """

    owner = None  # type: Optional[Company]
    """ (:py:class:`.Company` | None)  """

    latest = None  # type: Optional[bool]
    """ (bool|None) true if version is latest or for master versions without versions,
    false otherwise.
    """

    stats = None  # type: Optional[ProductStats]
    """ (:py:class:``.ProductStats) Statistics of product use, depends on account of callee. """

    # Undocumented fields (they appear in PHP SDK)

    status = None  # type: str
    """ (str) Product status. """

    def get_templates(self, config=None):
        """
        :param Config config: Configuration to use, or None for environment config.
        :return: List of all templates associated with the product.
        :rtype: List[Template]
        """
        text, _ = ApiClient(config or Config.get_instance(),
                            'products/' + self.id + '/templates').get()
        return Template.deserialize(text)

    def get_product_configurations(self, filters=None, config=None):
        """
        :param dict|Query filters: Filters for the requests. Supported filters are:
          - ``parameter.id``
          - ``parameter.title``
          - ``parameter.scope``
          - ``marketplace.id``
          - ``marketplace.name``
          - ``item.id``
          - ``item.name``
          - ``value``
        :param Config config: Configuration to use, or None for environment config.
        :return: A list with the product configuration parameter data.
        :rtype: List[ProductConfigurationParameter]
        """
        query = copy(filters) if isinstance(filters, Query) else Query(filters)
        text, _ = ApiClient(config or Config.get_instance(),
                            'products/' + self.id + '/configurations' + query.compile()).get()
        return ProductConfigurationParameter.deserialize(text)
