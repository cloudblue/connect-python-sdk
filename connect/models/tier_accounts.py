# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import Optional

from .base import BaseModel
from .tier_account import TierAccount
from .schemas import TierAccountsSchema


class TierAccounts(BaseModel):
    """ TierAccounts object. """

    _schema = TierAccountsSchema()

    customer = None  # type: TierAccount
    """ (:py:class:`.TierAccount`) Customer Level TierAccount Object. """

    tier1 = None  # type: TierAccount
    """ (:py:class:`.TierAccount`) Level 1 TierAccount Object. """

    tier2 = None  # type: Optional[TierAccount]
    """ (:py:class:`.TierAccount` | None) Level 2 TierAccount Object. """
