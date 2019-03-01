from marshmallow import Schema, fields, post_load

from .base import BaseModel, BaseSchema


class Hub(BaseModel):
    pass


class HubSchema(BaseSchema):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Hub(**data)


class HubsSchemaMixin(Schema):
    hub = fields.Nested(HubSchema, only=('id', 'name'))
    external_id = fields.Str()
