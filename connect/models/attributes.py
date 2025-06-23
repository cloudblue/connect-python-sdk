# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import AttributesSchema


class Attributes(BaseModel):
    """ Attributes object. """

    _schema = AttributesSchema()

    vendor = None  # type: object
    """ (obj) Attributes Vendor. """

    provider = None  # type: object
    """ (obj) Attributes Provider. """
