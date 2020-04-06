# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import List, Optional

from .base import BaseModel
from .product_family import ProductFamily
from .schemas import ProductCategorySchema


class ProductCategory(BaseModel):
    """ Represents a product category. """

    _schema = ProductCategorySchema()

    name = None  # type: str
    """ (str) Category name. """

    parent = None  # type: Optional[ProductCategory]
    """ (:py:class:`.ProductCategory` | None) Reference to parent category. """

    children = None  # type: Optional[List[ProductCategory]]
    """ (List[:py:class:`.ProductCategory`] | None)  List of children categories. """

    family = None  # type: Optional[ProductFamily]
    """ (:py:class:`.ProductFamily` | None) Product family. """
