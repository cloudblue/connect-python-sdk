from marshmallow import fields, post_load

from .base import BaseObject, BaseScheme


class Company(BaseObject):
    pass


class CompanyScheme(BaseScheme):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Company(**data)
