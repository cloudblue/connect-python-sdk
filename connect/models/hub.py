# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import Optional

from .base import BaseModel
from .company import Company
from .event import Events
from connect.models.schemas import HubInstanceSchema, HubStatsSchema, HubSchema, ExtIdHubSchema


class HubInstance(BaseModel):
    """ An instance of a hub. """

    _schema = HubInstanceSchema()

    type = None  # type: str
    """ (str) E-Commerce system type. """


class HubStats(BaseModel):
    """ Hub stats. """

    _schema = HubStatsSchema()

    connections = None  # type: int
    """ (int) Number of connections active for this Hub. """

    marketplaces = None  # type: int
    """ (int) Number of marketplaces for this Hub. """


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


class ExtIdHub(BaseModel):
    """ Associates a :py:class:`.Hub` with an external id. """

    _schema = ExtIdHubSchema()

    hub = None  # type: Hub
    """ (:py:class:`.Hub`) Hub. """

    external_id = None  # type: str
    """ (str) External id. """
