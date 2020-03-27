# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

import datetime
from typing import Optional

from .base import BaseModel
from .schemas import StatSchema


class Stat(BaseModel):
    """ Stats object. """

    _schema = StatSchema()

    count = None # type: Int
    """ (Int) Count. """

    last_request = None # type: last_request
    """ (:py:class:`.LastRequest`) Last Request. """
