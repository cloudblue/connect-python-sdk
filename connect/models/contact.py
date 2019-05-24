# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import fields, post_load
from typing import Optional

from .base import BaseModel, BaseSchema


class PhoneNumber(BaseModel):
    country_code = None  # type: Optional[str]
    """ (str|None) Country code. """

    area_code = None  # type: Optional[str]
    """ (str|None) Area code. """

    phone_number = None  # type: Optional[str]
    """ (str|None) Phone number. """

    extension = None  # type: Optional[str]
    """ (str|None) Phone extension. """


class PhoneNumberSchema(BaseSchema):
    country_code = fields.Str(allow_none=True)
    area_code = fields.Str(allow_none=True)
    phone_number = fields.Str(allow_none=True)
    extension = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        return PhoneNumber(**data)


class Contact(BaseModel):
    """ Person of contact. """

    first_name = None  # type: Optional[str]
    """ (str|None) First name. """

    last_name = None  # type: Optional[str]
    """ (str|None) Last name. """

    email = None  # type: str
    """ (str) Email address. """

    phone_number = None  # type: PhoneNumber
    """ (:py:class:`.PhoneNumber`) Phone number."""


class ContactSchema(BaseSchema):
    email = fields.Str()
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    phone_number = fields.Nested(PhoneNumberSchema)

    @post_load
    def make_object(self, data):
        return Contact(**data)


class ContactInfo(BaseModel):
    """ Represents the information of a contact. """

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


class ContactInfoSchema(BaseSchema):
    address_line1 = fields.Str()
    address_line2 = fields.Str(allow_none=True)
    city = fields.Str()
    contact = fields.Nested(ContactSchema)
    country = fields.Str()
    postal_code = fields.Str()
    state = fields.Str()

    @post_load
    def make_object(self, data):
        return ContactInfo(**data)
