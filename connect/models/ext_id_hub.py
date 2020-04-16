# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .hub import Hub
from .schemas import ExtIdHubSchema


class ExtIdHub(BaseModel):
    """ Associates a :py:class:`.Hub` with an external id. """

    _schema = ExtIdHubSchema()

    hub = None  # type: Hub
    """ (:py:class:`.Hub`) Hub. """

    external_id = None  # type: str
    """ (str) External id. """
