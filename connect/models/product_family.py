# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import ProductFamilySchema


class ProductFamily(BaseModel):
    """ Represents a family of products """

    _schema = ProductFamilySchema()

    name = None  # type: str
    """ (str) Family name. """
