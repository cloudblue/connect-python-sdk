# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import UsageRecordsSchema


class UsageRecords(BaseModel):
    """ Usage Records Object. """
    # TODO: Verify that this data is correct.

    _schema = UsageRecordsSchema()

    valid = None  # type: int
    """ (int) Valid. """

    invalid = None  # type: int
    """ (int) Invalid. """
