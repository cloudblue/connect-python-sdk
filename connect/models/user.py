# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import UserSchema


class User(BaseModel):
    """ Represents a user within the platform. """

    _schema = UserSchema()

    name = None  # type: str
    """ (str) User name. """

    email = None  # type: str
    """ (str) User email. """
