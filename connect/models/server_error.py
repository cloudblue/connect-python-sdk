from marshmallow import Schema, fields, post_load

from .base import BaseModel


class ServerError(BaseModel):
    pass


class ServerErrorSchema(Schema):
    error_code = fields.Str()
    params = fields.Dict()
    errors = fields.List(fields.Str())

    @post_load
    def make_object(self, data):
        return ServerError(**data)
