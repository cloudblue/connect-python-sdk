# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from connect.models.schemas import CompanySchema, UserSchema


class Company(BaseModel):
    """ Represents a company within the platform. """

    _schema = CompanySchema()

    name = None  # type: str
    """ (str) Company name. """


class User(BaseModel):
    """ Represents a user within the platform. """

    _schema = UserSchema()

    name = None  # type: str
    """ (str) User name. """
