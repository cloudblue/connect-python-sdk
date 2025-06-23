# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

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
