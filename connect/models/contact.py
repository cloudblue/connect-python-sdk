# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import Optional

from .base import BaseModel
from .phone_number import PhoneNumber
from .schemas import ContactSchema


class Contact(BaseModel):
    """ Person of contact. """

    _schema = ContactSchema()

    first_name = None  # type: Optional[str]
    """ (str|None) First name. """

    last_name = None  # type: Optional[str]
    """ (str|None) Last name. """

    email = None  # type: str
    """ (str) Email address. """

    phone_number = None  # type: PhoneNumber
    """ (:py:class:`.PhoneNumber`) Phone number."""
