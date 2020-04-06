# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import TemplateSchema


class Template(BaseModel):
    """ Tier Template """

    _schema = TemplateSchema()

    name = None  # type: str
    """ (str) Template name. """

    representation = None  # type: str
    """ (str) Template representation. """

    body = None  # type: str
    """ (str) Template body. """
