# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import Optional

from .base import BaseModel
from connect.models.schemas import PhoneNumberSchema, ContactSchema, ContactInfoSchema


class PhoneNumber(BaseModel):
    """ Phone number. """

    _schema = PhoneNumberSchema()

    country_code = None  # type: Optional[str]
    """ (str|None) Country code. """

    area_code = None  # type: Optional[str]
    """ (str|None) Area code. """

    phone_number = None  # type: Optional[str]
    """ (str|None) Phone number. """

    extension = None  # type: Optional[str]
    """ (str|None) Phone extension. """


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


class ContactInfo(BaseModel):
    """ Represents the information of a contact. """

    _schema = ContactInfoSchema()

    address_line1 = None  # type: str
    """ (str) Street address, first line. """

    address_line2 = None  # type: Optional[str]
    """ (str|None) Street address, second line. """

    country = None  # type: str
    """ (str) Country code. """

    state = None  # type: str
    """ (str) State name. """

    city = None  # type: str
    """ (str) City name. """

    postal_code = None  # type: str
    """ (str) Postal ZIP code. """

    contact = None  # type: Contact
    """ (:py:class:`.Contact`) Person of contact. """
