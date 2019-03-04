# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import Schema, fields, post_load
from typing import List

from .base import BaseModel


class ServerError(BaseModel):
    error_code = None  # type: str
    params = None  # type: dict
    errors = None  # type: List[str]


class ServerErrorSchema(Schema):
    error_code = fields.Str()
    params = fields.Dict()
    errors = fields.List(fields.Str())

    @post_load
    def make_object(self, data):
        return ServerError(**data)
