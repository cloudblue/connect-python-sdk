# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

import datetime
from typing import Optional

from .base import BaseModel
from .schemas import StatsSchema


class Stats(BaseModel):
    """ Stats object. """

    _schema = StatsSchema()

    vendor = None # type: Company
    """ (:py:class:`.Company`) Vendor. """

    provider = None # type: Company
    """ (:py:class:`.Company`) Provider. """
