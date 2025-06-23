# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import UnitSchema


class Unit(BaseModel):
    """ Unit object. """

    _schema = UnitSchema()

    title = None  # type: str
    """ (str) Name of measure unit. """

    unit = None  # type: str
    """ (str) unit code of measure unit. """
