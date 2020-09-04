# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import UnitSchema


class Unit(BaseModel):
    """ Unit object. """

    _schema = UnitSchema()

    title = None  # type: str
    """ (str) Name of measure unit. """

    unit = None  # type: str
    """ (str) unit code of measure unit. """
