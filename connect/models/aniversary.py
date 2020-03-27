# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import AniversarySchema

class Aniversary(BaseModel):
    """ An Aniversary object. """

    _schema = AniversarySchema()

    day = None  # type: str
    """ (str) Day of the aniversay. """

    month = None  # type: str
    """ (str) Month of the aniversary. """