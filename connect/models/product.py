# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import datetime
from typing import List, Optional, Union

from .base import BaseModel
from connect.models.schemas import ProductConfigurationSchema, DownloadLinkSchema, DocumentSchema,\
    CustomerUiSettingsSchema, ProductSchema, RenewalSchema, ItemSchema


class ProductConfiguration(BaseModel):
    """ Product configurations. """

    _schema = ProductConfigurationSchema()

    suspend_resume_supported = None  # type: bool
    """ (bool) Is suspend and resume supported for the product? """

    requires_reseller_information = None  # type: bool
    """ (bool) Does the product require reseller information? """


class DownloadLink(BaseModel):
    """ Download link for a product. """

    _schema = DownloadLinkSchema()

    title = None  # type: str
    """ (str) Link title. """

    url = None  # type: str
    """ (str) Link URL. """


class Document(BaseModel):
    """ Document for a product. """

    _schema = DocumentSchema()

    title = None  # title: str
    """ (str) Document title. """

    url = None  # title: str
    """ (str) Document URL. """

    visible_for = None  # title: str
    """ (str) Document visibility. One of: admin, user. """


class CustomerUiSettings(BaseModel):
    """ Customer Ui Settings for a product. """

    _schema = CustomerUiSettingsSchema()

    description = None  # type: str
    """ (str) Description. """

    getting_started = None  # type: str
    """ (str) Getting started. """

    download_links = None  # type: List[DownloadLink]
    """ (List[:py:class:`.DownloadLink`]) Download links. """

    documents = None  # type: List[Document]
    """ (List[:py:class:`.Document`]) Documents. """


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

    configurations = None  # type: ProductConfiguration
    """ (:py:class:`.ProductConfiguration`) Product configuration. """

    customer_ui_settings = None  # type: CustomerUiSettings
    """ (:py:class:`.CustomerUiSettings`) Customer Ui Settings. """


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

    global_id = None  # type: str
    """ (str) Global id. """

    # Undocumented fields (they appear in PHP SDK)

    period = None  # type: str
    """ (str) Period. """
