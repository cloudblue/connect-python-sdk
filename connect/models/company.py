# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import CompanySchema


class Company(BaseModel):
    """ Represents a company within the platform. """

    _schema = CompanySchema()

    name = None  # type: str
    """ (str) Company name. """
