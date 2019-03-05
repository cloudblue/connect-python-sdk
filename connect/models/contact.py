# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema


class PhoneNumber(BaseModel):
    country_code = None  # type: str
    area_code = None  # type: str
    phone_number = None  # type: str
    extension = None  # type: str


class PhoneNumberSchema(BaseSchema):
    country_code = fields.Str()
    area_code = fields.Str()
    phone_number = fields.Str()
    extension = fields.Str()

    @post_load
    def make_object(self, data):
        return PhoneNumber(**data)


class Contact(BaseModel):
    email = None  # type: str
    first_name = None  # type: str
    last_name = None  # type: str
    phone_number = None  # type: PhoneNumber


class ContactSchema(BaseSchema):
    email = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    phone_number = fields.Nested(PhoneNumberSchema)

    @post_load
    def make_object(self, data):
        return Contact(**data)


class ContactInfo(BaseModel):
    address_line1 = None  # type: str
    address_line2 = None  # type: str
    city = None  # type: str
    contact = None  # type: Contact
    country = None  # type: str
    postal_code = None  # type: str
    state = None  # type: str


class ContactInfoSchema(BaseSchema):
    address_line1 = fields.Str()
    address_line2 = fields.Str()
    city = fields.Str()
    contact = fields.Nested(ContactSchema)
    country = fields.Str()
    postal_code = fields.Str()
    state = fields.Str()

    @post_load
    def make_object(self, data):
        return ContactInfo(**data)
