from marshmallow import Schema, fields, post_load

from .base import BaseObject, BaseScheme


class Tier(BaseObject):
    pass


class TierScheme(BaseScheme):
    name = fields.Str()
    contact_info = fields.Dict()
    external_id = fields.Str()
    external_uid = fields.UUID()

    @post_load
    def make_object(self, data):
        return Tier(**data)


class TiersSchemeMixin(Schema):
    customer = fields.Nested(TierScheme)
    tier1 = fields.Nested(TierScheme)
    tier2 = fields.Nested(TierScheme)
