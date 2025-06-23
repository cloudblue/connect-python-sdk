# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import HubInstanceSchema


class HubInstance(BaseModel):
    """ An instance of a hub. """

    _schema = HubInstanceSchema()

    type = None  # type: str
    """ (str) E-Commerce system type. """
