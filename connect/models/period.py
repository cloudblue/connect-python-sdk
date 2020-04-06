# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import datetime
from typing import Optional

from .base import BaseModel
from .schemas import PeriodSchema


class Period(BaseModel):
    """ Period object. """

    _schema = PeriodSchema()

    period_from = None  # type: Optional[datetime.date]
    """ (datetime.date) Period From. """

    period_to = None  # type: Optional[datetime.date]
    """ (datetime.date) Period To. """

    delta = None  # type: str
    """ (string) Period Delta. """

    uom = None  # type: str
    """ (string) Period uom. """
