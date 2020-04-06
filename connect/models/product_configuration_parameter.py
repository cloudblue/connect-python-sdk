# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .constraints import Constraints
from .events import Events
from .item import Item
from .marketplace import Marketplace
from .param import Param
from .schemas import ProductConfigurationParameterSchema


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
