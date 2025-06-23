# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import CountrySchema


class Country(BaseModel):
    """ Country data. """

    _schema = CountrySchema()

    name = None  # type: str
    """ (str) Country name. """

    icon = None  # type: str
    """ (str) Icon path. """

    zone = None  # type: str
    """ (str) Geographical zone. """
