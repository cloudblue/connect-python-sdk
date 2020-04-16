# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import StatsSchema


class Stats(BaseModel):
    """ Stats object. """

    _schema = StatsSchema()

    vendor = None  # type: object
    """ (:py:class:`.Company`) Vendor. """

    provider = None  # type: object
    """ (:py:class:`.Company`) Provider. """
