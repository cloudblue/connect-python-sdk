# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import Optional

from .base import BaseModel
from .contact import Contact
from .schemas import ContactInfoSchema


class ContactInfo(BaseModel):
    """ Represents the information of a contact. """

    _schema = ContactInfoSchema()

    address_line1 = None  # type: str
    """ (str) Street address, first line. """

    address_line2 = None  # type: Optional[str]
    """ (str|None) Street address, second line. """

    country = None  # type: str
    """ (str) Country code. """

    state = None  # type: Optional[str]
    """ (str) State name. """

    city = None  # type: str
    """ (str) City name. """

    postal_code = None  # type: str
    """ (str) Postal ZIP code. """

    contact = None  # type: Contact
    """ (:py:class:`.Contact`) Person of contact. """
