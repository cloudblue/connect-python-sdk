from marshmallow import Schema, fields, post_load


class BaseObject:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        if kwargs:
            for attr, val in kwargs.items():
                setattr(self, attr, val)


class BaseScheme(Schema):
    id = fields.Str()

    @post_load
    def make_object(self, data):
        return BaseObject(**data)


class Product(BaseObject):
    pass


class ProductScheme(BaseScheme):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Product(**data)


class Item(BaseObject):
    pass


class ItemScheme(BaseScheme):
    global_id = fields.Str()
    mpn = fields.Str()
    old_quantity = fields.Str()
    quantity = fields.Integer()

    @post_load
    def make_object(self, data):
        return Item(**data)


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


class Company(BaseObject):
    pass


class CompanyScheme(BaseScheme):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        return Company(**data)


class Connection(BaseObject):
    pass


class ConnectionScheme(BaseScheme):
    type = fields.Str()
    provider = fields.Nested(CompanyScheme, only=('id', 'name'))
    vendor = fields.Nested(CompanyScheme, only=('id', 'name'))
    product = fields.Nested(ProductScheme)
    hub = fields.Nested(HubScheme)

    @post_load
    def make_object(self, data):
        return Connection(**data)


class ValueChoice(BaseObject):
    pass


class ValueChoiceScheme(Schema):
    value = fields.Str()
    label = fields.Str()

    @post_load
    def make_object(self, data):
        return ValueChoice(**data)


class Param(BaseObject):
    pass


class ParamsScheme(BaseScheme):
    name = fields.Str()
    type = fields.Str()
    value = fields.Str()
    value_choices = fields.List(fields.Nested(ValueChoiceScheme))
    value_error = fields.Str()

    @post_load
    def make_object(self, data):
        return Param(**data)


class Asset(BaseObject):
    pass


class AssetScheme(BaseScheme):
    status = fields.Str()
    external_id = fields.Str()
    external_uid = fields.UUID()
    product = fields.Nested(ProductScheme, only=('id', 'name'))
    connection = fields.Nested(
        ConnectionScheme, only=('id', 'type', 'provider', 'vendor'),
    )
    items = fields.List(fields.Nested(ItemScheme))
    params = fields.List(fields.Nested(ParamsScheme))
    tiers = fields.Nested(TiersSchemeMixin)

    @post_load
    def make_object(self, data):
        return Asset(**data)


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


class Fulfillment(BaseObject):
    pass


class FulfillmentScheme(BaseScheme):
    activation_key = fields.Str()
    asset = fields.Nested(AssetScheme)
    status = fields.Str()
    type = fields.Str()
    updated = fields.DateTime()
    created = fields.DateTime()
    reason = fields.Str()
    params_form_url = fields.Str()
    contract = fields.Nested(ContractScheme, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceScheme, only=('id', 'name'))

    @post_load
    def make_object(self, data):
        return Fulfillment(**data)


class ServerError(BaseObject):
    pass


class ServerErrorScheme(Schema):
    error_code = fields.Str()
    params = fields.Dict()
    errors = fields.List(fields.Str())

    @post_load
    def make_object(self, data):
        return ServerError(**data)
