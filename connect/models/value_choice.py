# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import ValueChoiceSchema


class ValueChoice(BaseModel):
    """ A value choice for a parameter. """

    _schema = ValueChoiceSchema()

    value = None  # type: str
    """ (str) Value. """

    label = None  # type: str
    """ (str) Label. """
