# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import StatsSchema


class Stats(BaseModel):
    """ Stats object. """

    _schema = StatsSchema()

    vendor = None  # type: object
    """ (:py:class:`.Company`) Vendor. """

    provider = None  # type: object
    """ (:py:class:`.Company`) Provider. """
