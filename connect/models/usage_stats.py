# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import UsageStatsSchema


class UsageStats(BaseModel):
    """ Usage Stats object. """

    _schema = UsageStatsSchema()

    uploaded = None  # type: int
    """ (Int) Uploaded. """

    validated = None  # type: int
    """ (Int) Validated. """

    pending = None  # type: int
    """ (Int) Pending. """

    accepted = None  # type: int
    """ (Int) Accepted. """

    closed = None  # type: int
    """ (Int) Closed. """
