# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import CommitmentSchema


class Commitment(BaseModel):
    """ Billing commitment object. """

    _schema = CommitmentSchema()

    multiplier = None  # type: str
    """ (str) Commitment multiplier. """

    count = None  # type: int
    """ (int) Number of commitments. """
