# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import json

from marshmallow import Schema, fields, post_load


class BaseModel(object):
    """ Base class of all models.

    All the arguments provided on creation of the model are injected as attributes on the object.
    """

    id = None  # type: str
    """ (str) Globally unique id. """

    def __init__(self, **kwargs):
        # Inject parsed properties in the model
        for attr, val in kwargs.items():
            setattr(self, attr, val)

    @property
    def json(self):
        """
        :return: The JSON representation of the model.
        :rtype: dict|list
        """
        dump = json.dumps(self, default=lambda o: getattr(o, '__dict__', str(o)))
        return json.loads(dump)


class BaseSchema(Schema):
    id = fields.Str()

    @post_load
    def make_object(self, data):
        return BaseModel(**data)
