# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import AttributesSchema


class Attributes(BaseModel):
    """ Attributes object. """

    _schema = AttributesSchema()

    vendor = None  # type: object
    """ (obj) Attributes Vendor. """

    provider = None  # type: object
    """ (obj) Attributes Provider. """
