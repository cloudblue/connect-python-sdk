# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import datetime
from typing import Optional

from .base import BaseModel
from .company import Company
from .customer_ui_settings import CustomerUiSettings
from .product_category import ProductCategory
from .product_configuration import ProductConfiguration
from .product_stats import ProductStats
from .schemas import ProductSchema


class ProductConfigurationParameter(BaseModel):
    """ Representation of Configuration Phase Parameter (CPP) Data object """

    _schema = ProductConfigurationParameterSchema()

    value = None  # type: str
    """ (str|None) Configuration parameter value. """

    parameter = None  # type: Param
    """ (:py:class:`.Param`) Full representation of parameter. """

    marketplace = None  # type: Marketplace
    """ (:py:class:`.Marketplace` | None) Reference to Marketplace. """

    item = None  # type: Item
    """ (:py:class:`.Item` | None) Reference to Item. """

    events = None  # type: Events
    """ (:py:class:`.Events`) Product events. """

    # Undocumented fields (they appear in PHP SDK)

    constraints = None  # type: Constraints
    """ (:py:class:`.Constraints`) Constraints. """


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
        :param Dict[str, Any] filters: Filters for the requests. Supported filters are:
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
        text, _ = ApiClient(config or Config.get_instance(),
                            'products/' + self.id + '/configurations').get(params=filters)
        return ProductConfigurationParameter.deserialize(text)


class Renewal(BaseModel):
    """ Item renewal data. """

    _schema = RenewalSchema()

    from_ = None  # type: datetime.datetime
    """ (datetime.datetime) Date of renewal beginning. """

    to = None  # type: datetime.datetime
    """ (datetime.datetime) Date of renewal end. """

    period_delta = None  # type: int
    """ (int) Size of renewal period. """

    period_uom = None  # type: str
    """ (str) Unit of measure for renewal period. One of: year, month, day, hour. """


class Item(BaseModel):
    """ A product item. """

    _schema = ItemSchema()

    mpn = None  # type: str
    """ (str) Item manufacture part number. """

    quantity = None  # type: Union[int,float]
    """ (int|float) Number of items of the type in the asset (-1 if unlimited) """

    old_quantity = None  # type: Union[int,float,None]
    """ (int|float|None) Previous value of quantity. """

    renewal = None  # type: Optional[Renewal]
    """ (:py:class:`.Renewal` | None) Parameters of renewal request
    (empty for all other types).
    """

    params = None  # type: List[connect.models.Param]
    """ (List[:py:class:`.Param` | None] List of Item and Item x Marketplace Configuration Phase
    Parameter Context-Bound Object
    """

    # Undocumented fields (they appear in PHP SDK)

    display_name = None  # type: str
    """ (str) Display name. """

    global_id = None  # type: str
    """ (str) Global id. """

    item_type = None  # type: str
    """ (str) Item type. """

    period = None  # type: str
    """ (str) Period. """

    type = None  # type: str
    """ (str) Type. """

    name = None  # type: str
    """ (str) Name. """

    def get_param_by_id(self, param_id):
        """
        :param str param_id: Id of the parameter.
        :return: A Param by ID, or None if it was not found.
        :rtype: Param
        """
        try:
            return list(filter(lambda p: p.id == param_id, self.params))[0]
        except IndexError:
            return None
