from marshmallow import Schema, fields, post_load

from .base import BaseObject


class ServerError(BaseObject):
    pass


class ServerErrorScheme(Schema):
    error_code = fields.Str()
    params = fields.Dict()
    errors = fields.List(fields.Str())

    @post_load
    def make_object(self, data):
        return ServerError(**data)
