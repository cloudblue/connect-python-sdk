# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

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
