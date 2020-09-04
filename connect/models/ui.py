# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import UISchema


class UI(BaseModel):
    """ UI object. """

    _schema = UISchema()

    visibility = None  # type: bool
    """ (str) Item UI visibility. """
