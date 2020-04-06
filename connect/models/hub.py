# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import Optional

from .base import BaseModel
from .company import Company
from .events import Events
from .hub_instance import HubInstance
from .hub_stats import HubStats
from .schemas import HubSchema


class Hub(BaseModel):
    """ A Hub. """

    _schema = HubSchema()

    name = None  # type: str
    """ (str) Hub name. """

    company = None  # type: Company
    """ (:py:class:`.Company`) Reference to the company the hub belongs to. """

    description = None  # type: Optional[str]
    """ (str|None) Hub description (Markdown text). """

    instance = None  # type: HubInstance
    """ (:py:class:`.HubInstance`) Hub instance. """

    events = None  # type: Events
    """ (:py:class:`.Events`) Events occurred on Hub. """

    stats = None  # type: HubStats
    """ (:py:class:`.HubStats`) Hub stats. """
