from marshmallow import fields, post_load

from .base import BaseObject, BaseScheme
from .company import CompanyScheme
from .hub import HubsSchemeMixin


class Marketplace(BaseObject):
    pass


class MarketplaceScheme(BaseScheme):
    name = fields.Str()
    zone = fields.Str()
    description = fields.Str()
    active_contract = fields.Int()
    icon = fields.Str()
    owner = fields.Nested(CompanyScheme, only=('id', 'name'))
    hubs = fields.List(fields.Nested(HubsSchemeMixin, only=('id', 'name')))

    @post_load
    def make_object(self, data):
        return Marketplace(**data)


class Agreement(BaseObject):
    pass


class AgreementScheme(BaseScheme):
    type = fields.Str()
    title = fields.Str()
    description = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    owner = fields.Nested(CompanyScheme, only=('id', 'name'))
    stats = fields.Dict()
    active = fields.Bool()
    version = fields.Int()
    link = fields.Str()
    version_created = fields.DateTime()
    version_contracts = fields.Int()

    @post_load
    def make_object(self, data):
        return Agreement(**data)


class Contract(BaseObject):
    pass


class ContractScheme(BaseScheme):
    name = fields.Str()
    status = fields.Str()
    version = fields.Int()
    type = fields.Str()
    agreement = fields.Nested(AgreementScheme, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceScheme, only=('id', 'name'))
    owner = fields.Nested(CompanyScheme, only=('id', 'name'))
    creater = fields.Nested(CompanyScheme, only=('id', 'name'))
    created = fields.DateTime()
    updated = fields.DateTime()
    enrolled = fields.Str()
    version_created = fields.DateTime()
    activation = fields.Dict()
    signee = fields.Nested(CompanyScheme, only=('id', 'name'))

    @post_load
    def make_object(self, data):
        return Contract(**data)
