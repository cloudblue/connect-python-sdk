from marshmallow import Schema, fields, post_load

from .base import BaseObject, BaseScheme


class Hub(BaseObject):
    pass


class HubScheme(BaseScheme):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Hub(**data)


class HubsSchemeMixin(Schema):
    hub = fields.Nested(HubScheme, only=('id', 'name'))
    external_id = fields.Str()
