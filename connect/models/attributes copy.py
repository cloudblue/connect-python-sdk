# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

import datetime
from typing import Optional

from .base import BaseModel
from .schemas import AttributesSchema


class Attributes(BaseModel):
    """ Activation object. """

    _schema = AttributesSchema()

    vendor = None  # type: obj
    """ (obj) Attributes Vendor. """

    provider = None  # type: obj
    """ (obj) Attributes Provider. """
