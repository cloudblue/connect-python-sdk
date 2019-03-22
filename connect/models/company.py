# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema


class Company(BaseModel):
    name = None  # type: str


class CompanySchema(BaseSchema):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Company(**data)
