# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from marshmallow import Schema, fields, post_load


class BaseModel:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        if kwargs:
            for attr, val in kwargs.items():
                setattr(self, attr, val)

    @staticmethod
    def _get_by_id(objects, identity):
        try:
            return list(filter(lambda obj: obj.id == identity, objects))[0]
        except IndexError:
            return None


class BaseSchema(Schema):
    id = fields.Str()

    @post_load
    def make_object(self, data):
        return BaseModel(**data)
