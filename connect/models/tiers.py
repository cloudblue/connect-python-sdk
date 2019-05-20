# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .contact import ContactInfo
from connect.models.schemas import TierSchema, TiersSchema


class Tier(BaseModel):
    """ Tier Object. """

    _schema = TierSchema()

    name = None  # type: str
    """ (str) Tier name. """

    contact_info = None  # type: ContactInfo
    """ (:py:class:`.ContactInfo`) Tier Contact Object. """

    external_id = None  # type: str
    """ (str) External id. """

    external_uid = None  # type: str
    """ (str) External uid. """


class Tiers(BaseModel):
    """ Tiers object. """

    _schema = TiersSchema()

    customer = None  # type: Tier
    """ (:py:class:`.Tier`) Customer Level Tier Object. """

    tier1 = None  # type: Tier
    """ (:py:class:`.Tier`) Level 1 Tier Object. """

    tier2 = None  # type: Tier
    """ (:py:class:`.Tier`) Level 2 Tier Object. """
