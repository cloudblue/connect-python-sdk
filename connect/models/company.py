from marshmallow import fields, post_load

from .base import BaseModel, BaseSchema


class Company(BaseModel):
    pass


class CompanySchema(BaseSchema):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Company(**data)
