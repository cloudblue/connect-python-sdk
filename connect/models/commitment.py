# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import CommitmentSchema


class Commitment(BaseModel):
    """ Billing commitment object. """

    _schema = CommitmentSchema()

    multiplier = None  # type: str
    """ (str) Commitment multiplier. """

    count = None  # type: int
    """ (int) Number of commitments. """
