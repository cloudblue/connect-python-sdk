# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import Optional

from .base import BaseModel
from .contact_info import ContactInfo
from .schemas import TierAccountSchema


class TierAccount(BaseModel):
    """ Tier account. """

    _schema = TierAccountSchema()

    name = None  # type: str
    """ (str) Tier name. """

    contact_info = None  # type: ContactInfo
    """ (:py:class:`.ContactInfo`) Tier Contact Object. """

    external_id = None  # type: Optional[str]
    """ (str|None) Only in case of filtering by this field. """

    external_uid = None  # type: Optional[str]
    """ (str|None) Only in case of filtering by this field. """
