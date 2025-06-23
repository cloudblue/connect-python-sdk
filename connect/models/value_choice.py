# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import ValueChoiceSchema


class ValueChoice(BaseModel):
    """ A value choice for a parameter. """

    _schema = ValueChoiceSchema()

    value = None  # type: str
    """ (str) Value. """

    label = None  # type: str
    """ (str) Label. """
