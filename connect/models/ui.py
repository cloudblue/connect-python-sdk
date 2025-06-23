# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import UISchema


class UI(BaseModel):
    """ UI object. """

    _schema = UISchema()

    visibility = None  # type: bool
    """ (str) Item UI visibility. """
