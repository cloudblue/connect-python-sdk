# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import Optional

from .base import BaseModel
from .schemas import PhoneNumberSchema


class PhoneNumber(BaseModel):
    """ Phone number. """

    _schema = PhoneNumberSchema()

    country_code = None  # type: Optional[str]
    """ (str|None) Country code. """

    area_code = None  # type: Optional[str]
    """ (str|None) Area code. """

    phone_number = None  # type: Optional[str]
    """ (str|None) Phone number. """

    extension = None  # type: Optional[str]
    """ (str|None) Phone extension. """
