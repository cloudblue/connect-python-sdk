# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import HubInstanceSchema


class HubInstance(BaseModel):
    """ An instance of a hub. """

    _schema = HubInstanceSchema()

    type = None  # type: str
    """ (str) E-Commerce system type. """
