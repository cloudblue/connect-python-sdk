# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import Optional

from .base import BaseModel
from .schemas import AgreementStatsSchema


class AgreementStats(BaseModel):
    """ Agreement stats. """

    _schema = AgreementStatsSchema()

    contracts = None  # type: Optional[int]
    """ (int|None) Number of contracts this agreement has. """

    versions = None  # type: int
    """ (int) Number of versions in the agreement. """
