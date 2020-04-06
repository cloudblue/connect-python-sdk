# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import HubStatsSchema


class HubStats(BaseModel):
    """ Hub stats. """

    _schema = HubStatsSchema()

    connections = None  # type: int
    """ (int) Number of connections active for this Hub. """

    marketplaces = None  # type: int
    """ (int) Number of marketplaces for this Hub. """
