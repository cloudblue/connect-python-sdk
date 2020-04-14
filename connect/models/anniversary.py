# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import AnniversarySchema


class Anniversary(BaseModel):
    """ An Anniversary object. """

    _schema = AnniversarySchema()

    day = None  # type: str
    """ (str) Day of the anniversay. """

    month = None  # type: str
    """ (str) Month of the anniversary. """
