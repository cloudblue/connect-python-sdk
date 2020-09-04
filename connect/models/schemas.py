# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from deprecation import deprecated
from marshmallow import Schema, fields, post_load
import six


class BaseSchema(Schema):

    def __init__(self, *args, **kwargs):
        # kwargs['strict'] = True
        super(BaseSchema, self).__init__(*args, **kwargs)

    id = fields.Str()

    # Set allow_none to True in all fields
    def on_bind_field(self, field_name, field_obj):
        super(BaseSchema, self).on_bind_field(field_name, field_obj)
        field_obj.allow_none = True

    @post_load
    def make_object(self, data):
        from connect.models import BaseModel
        return BaseModel(**data)


class ActivationSchema(BaseSchema):
    link = fields.Str()
    message = fields.Str()
    date = fields.DateTime()

    @post_load
    def make_object(self, data):
        from connect.models import Activation
        return Activation(**data)


class AgreementStatsSchema(BaseSchema):
    contracts = fields.Int()
    versions = fields.Int()

    @post_load
    def make_object(self, data):
        from connect.models import AgreementStats
        return AgreementStats(**data)


class PeriodSchema(BaseSchema):
    period_from = fields.DateTime(data_key='from')
    period_to = fields.DateTime(data_key='to')
    delta = fields.Decimal()
    uom = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Period
        return Period(**data)


class LastRequestSchema(BaseSchema):
    type = fields.String()
    period = fields.Nested(PeriodSchema)

    @post_load
    def make_object(self, data):
        from connect.models import LastRequest
        return LastRequest(**data)


class CompanySchema(BaseSchema):
    name = fields.Str()
    count = fields.Integer()

    @post_load
    def make_object(self, data):
        from connect.models import Company
        return Company(**data)


class PhoneNumberSchema(BaseSchema):
    country_code = fields.Str()
    area_code = fields.Str()
    phone_number = fields.Str()
    extension = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import PhoneNumber
        return PhoneNumber(**data)


class ContactSchema(BaseSchema):
    email = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    phone_number = fields.Nested(PhoneNumberSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Contact
        return Contact(**data)


class ContactInfoSchema(BaseSchema):
    address_line1 = fields.Str()
    address_line2 = fields.Str()
    city = fields.Str()
    contact = fields.Nested(ContactSchema)
    country = fields.Str()
    postal_code = fields.Str()
    state = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import ContactInfo
        return ContactInfo(**data)


class ValueChoiceSchema(BaseSchema):
    value = fields.Str()
    label = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import ValueChoice
        return ValueChoice(**data)


class ConstraintsSchema(BaseSchema):
    hidden = fields.Bool()
    required = fields.Bool()
    choices = fields.Nested(ValueChoiceSchema, many=True)
    unique = fields.Bool()
    reconciliation = fields.Bool()
    min_length = fields.Integer()
    max_length = fields.Integer()

    @post_load
    def make_object(self, data):
        from connect.models import Constraints
        return Constraints(**data)


class DocumentSchema(BaseSchema):
    title = fields.Str()
    url = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Document
        return Document(**data)


class DownloadLinkSchema(BaseSchema):
    title = fields.Str()
    url = fields.Str()
    visible_for = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import DownloadLink
        return DownloadLink(**data)


class UserSchema(BaseSchema):
    name = fields.Str()
    email = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import User
        return User(**data)


class EventSchema(BaseSchema):
    at = fields.DateTime()
    by = fields.Nested(UserSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Event
        return Event(**data)


class EventsSchema(BaseSchema):
    created = fields.Nested(EventSchema)
    inquired = fields.Nested(EventSchema)
    pended = fields.Nested(EventSchema)
    validated = fields.Nested(EventSchema)
    updated = fields.Nested(EventSchema)
    approved = fields.Nested(EventSchema)
    uploaded = fields.Nested(EventSchema)
    submitted = fields.Nested(EventSchema)
    accepted = fields.Nested(EventSchema)
    rejected = fields.Nested(EventSchema)
    closed = fields.Nested(EventSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Events
        return Events(**data)


class HubInstanceSchema(BaseSchema):
    type = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import HubInstance
        return HubInstance(**data)


class HubStatsSchema(BaseSchema):
    connections = fields.Int()
    marketplaces = fields.Int()

    @post_load
    def make_object(self, data):
        from connect.models import HubStats
        return HubStats(**data)


class HubSchema(BaseSchema):
    name = fields.Str()
    company = fields.Nested(CompanySchema)
    description = fields.Str()
    instance = fields.Nested(HubInstanceSchema)
    events = fields.Nested(EventsSchema)
    stats = fields.Nested(HubStatsSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Hub
        return Hub(**data)


class ExternalIdField(fields.Field):
    def _deserialize(self, value, attr=None, data=None):
        if isinstance(value, six.string_types):
            return value
        elif isinstance(value, int):
            return str(value)
        else:
            raise ValueError({attr: [u'Not a valid int or string.']})


class ExtIdHubSchema(BaseSchema):
    hub = fields.Nested(HubSchema)
    external_id = ExternalIdField()

    @post_load
    def make_object(self, data):
        from connect.models import ExtIdHub
        return ExtIdHub(**data)


class RenewalSchema(BaseSchema):
    from_ = fields.DateTime(load_from='from')
    to = fields.DateTime()
    period_delta = fields.Int()
    period_uom = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Renewal
        return Renewal(**data)


class QuantityField(fields.Field):
    def _deserialize(self, value, attr=None, data=None):
        if isinstance(value, six.string_types):
            if value == 'unlimited':
                return -1
            else:
                try:
                    float_val = float(value)
                    int_val = int(float_val)
                    return int_val if int_val == float_val else float_val
                except ValueError:
                    raise ValueError({
                        attr: [u'Not a valid string encoded number nor "unlimited".']
                    })
        elif isinstance(value, (int, float)):
            return value
        else:
            raise ValueError({attr: [u'Not a valid int, float or string.']})


class MarketplaceSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str()
    active_contracts = fields.Int()
    icon = fields.Str()
    owner = fields.Nested(CompanySchema)
    hubs = fields.Nested(ExtIdHubSchema, many=True)
    zone = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Marketplace
        return Marketplace(**data)


class CountrySchema(BaseSchema):
    name = fields.Str()
    icon = fields.Str()
    zone = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Country
        return Country(**data)


class ParamSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str()
    type = fields.Str()
    value = fields.Str()
    value_error = fields.Str()
    value_choice = fields.Str(many=True)
    title = fields.Str()
    scope = fields.Str()
    constraints = fields.Nested(ConstraintsSchema)
    value_choices = fields.Nested(ValueChoiceSchema, many=True)
    structured_value = fields.Dict()
    phase = fields.Str()
    reconciliation = fields.Bool()
    events = fields.Nested(EventsSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    countries = fields.Nested(CountrySchema, many=True)

    @post_load
    def make_object(self, data):
        from connect.models import Param
        return Param(**data)


class UISchema(BaseSchema):
    visibility = fields.Bool()
    @post_load
    def make_object(self, data):
        from connect.models import UI
        return UI(**data)


class UnitSchema(BaseSchema):
    title = fields.Str()
    unit = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Unit
        return Unit(**data)


class CommitmentSchema(BaseSchema):
    multiplier = fields.Str()
    count = fields.Int()

    @post_load
    def make_object(self, data):
        from connect.models import Commitment
        return Commitment(**data)


class ItemSchema(BaseSchema):
    mpn = fields.Str()
    quantity = QuantityField()
    old_quantity = QuantityField()
    renewal = fields.Nested(RenewalSchema)
    unit = fields.Nested(UnitSchema)
    commitment = fields.Nested(CommitmentSchema)
    params = fields.Nested(ParamSchema, many=True)
    display_name = fields.Str()
    global_id = fields.Str()
    item_type = fields.Str()
    description = fields.Str()
    period = fields.Str()
    type = fields.Str()
    name = fields.Str()
    ui = fields.Nested(UISchema)

    @post_load
    def make_object(self, data):
        from connect.models import Item
        return Item(**data)


class AgreementSchema(BaseSchema):
    type = fields.String()
    title = fields.Str()
    description = fields.String()
    created = fields.DateTime()
    updated = fields.DateTime()
    owner = fields.Nested(CompanySchema)
    stats = fields.Nested(AgreementStatsSchema)
    author = fields.Nested(UserSchema)
    version = fields.Int()
    active = fields.Bool()
    link = fields.Str()
    version_created = fields.DateTime()
    version_contracts = fields.Int()
    agreements = fields.Nested('AgreementSchema', many=True)
    parent = fields.Nested('AgreementSchema')
    marketplace = fields.Nested(MarketplaceSchema)
    name = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Agreement
        return Agreement(**data)


class ContractSchema(BaseSchema):
    name = fields.Str()
    version = fields.Int()
    type = fields.Str()
    status = fields.Str()
    agreement = fields.Nested(AgreementSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    owner = fields.Nested(CompanySchema)
    creator = fields.Nested(UserSchema)
    created = fields.DateTime()
    updated = fields.DateTime()
    enrolled = fields.DateTime()
    version_created = fields.DateTime()
    activation = fields.Nested(ActivationSchema)
    signee = fields.Nested(UserSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Contract
        return Contract(**data)


class ProductConfigurationSchema(BaseSchema):
    suspend_resume_supported = fields.Bool()
    requires_reseller_information = fields.Bool()

    @post_load
    def make_object(self, data):
        from connect.models import ProductConfiguration
        return ProductConfiguration(**data)


class CustomerUiSettingsSchema(BaseSchema):
    description = fields.Str()
    getting_started = fields.Str()
    download_links = fields.Nested(DownloadLinkSchema, many=True)
    documents = fields.Nested(DocumentSchema, many=True)

    @post_load
    def make_object(self, data):
        from connect.models import CustomerUiSettings
        return CustomerUiSettings(**data)


class ProductFamilySchema(BaseSchema):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import ProductFamily
        return ProductFamily(**data)


class ProductCategorySchema(BaseSchema):
    name = fields.Str()
    parent = fields.Nested('ProductCategorySchema')
    children = fields.Nested('ProductCategorySchema', many=True)
    family = fields.Nested(ProductFamilySchema)

    @post_load
    def make_object(self, data):
        from connect.models import ProductCategory
        return ProductCategory(**data)


class ProductStatsInfoSchema(BaseSchema):
    distribution = fields.Int()
    sourcing = fields.Int()

    @post_load
    def make_object(self, data):
        from connect.models import ProductStatsInfo
        return ProductStatsInfo(**data)


class ProductStatsSchema(BaseSchema):
    listing = fields.Int()
    agreements = fields.Nested(ProductStatsInfoSchema)
    contracts = fields.Nested(ProductStatsInfoSchema)

    @post_load
    def make_object(self, data):
        from connect.models import ProductStats
        return ProductStats(**data)


class ProductConfigurationParameterSchema(BaseSchema):
    value = fields.Str()
    parameter = fields.Nested(ParamSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    item = fields.Nested(ItemSchema)
    events = fields.Nested(EventsSchema)
    constraints = fields.Nested(ConstraintsSchema)

    @post_load
    def make_object(self, data):
        from connect.models import ProductConfigurationParameter
        return ProductConfigurationParameter(**data)


class ProductSchema(BaseSchema):
    name = fields.Str()
    icon = fields.Str()
    short_description = fields.Str()
    detailed_description = fields.Str()
    version = fields.Int()
    published_at = fields.DateTime()
    configurations = fields.Nested(ProductConfigurationSchema)
    customer_ui_settings = fields.Nested(CustomerUiSettingsSchema)
    category = fields.Nested(ProductCategorySchema)
    owner = fields.Nested(CompanySchema)
    latest = fields.Bool()
    stats = fields.Nested(ProductStatsSchema)
    status = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Product
        return Product(**data)


class ServerErrorResponseSchema(BaseSchema):
    error_code = fields.Str()
    params = fields.Dict()
    errors = fields.List(fields.Str())

    @post_load
    def make_object(self, data):
        from connect.models import ServerErrorResponse
        return ServerErrorResponse(**data)


class TemplateSchema(BaseSchema):
    name = fields.Str()
    representation = fields.Str()
    body = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Template
        return Template(**data)


class ConfigurationSchema(BaseSchema):
    params = fields.Nested(ParamSchema, many=True)

    @post_load
    def make_object(self, data):
        from connect.models import Configuration
        return Configuration(**data)


class TierAccountSchema(BaseSchema):
    name = fields.Str()
    contact_info = fields.Nested(ContactInfoSchema)
    external_id = ExternalIdField()
    external_uid = fields.Str()
    environment = fields.Str()
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name', 'icon'))
    hub = fields.Nested(HubSchema, only=('id', 'name'))
    version = fields.Int()
    tax_id = fields.Str()

    events = fields.Nested(EventsSchema)
    scopes = fields.List(fields.Str())

    @post_load
    def make_object(self, data):
        from connect.models import TierAccount
        return TierAccount(**data)


class TierAccountsSchema(BaseSchema):
    customer = fields.Nested(TierAccountSchema)
    tier1 = fields.Nested(TierAccountSchema)
    tier2 = fields.Nested(TierAccountSchema)

    @post_load
    def make_object(self, data):
        from connect.models import TierAccounts
        return TierAccounts(**data)


class TierAccountRequestSchema(BaseSchema):
    type = fields.Str()
    status = fields.Str()
    account = fields.Nested(TierAccountSchema)
    provider = fields.Nested(CompanySchema, only=('id', 'name'))
    vendor = fields.Nested(CompanySchema, only=('id', 'name'))
    product = fields.Nested(ProductSchema, only=('id', 'icon', 'name', 'status'))
    reason = fields.Str()
    contact_info = fields.Nested(ContactInfoSchema)
    external_id = ExternalIdField()
    external_uid = fields.Str()
    events = fields.Nested(EventsSchema)

    @post_load
    def make_object(self, data):
        from connect.models import TierAccountRequest
        return TierAccountRequest(**data)


class ConnectionSchema(BaseSchema):
    type = fields.Str()
    provider = fields.Nested(CompanySchema)
    vendor = fields.Nested(CompanySchema)
    product = fields.Nested(ProductSchema)
    hub = fields.Nested(HubSchema)
    status = fields.Str()
    created_at = fields.DateTime()

    @post_load
    def make_object(self, data):
        from connect.models import Connection
        return Connection(**data)


class AssetSchema(BaseSchema):
    status = fields.Str()
    external_id = ExternalIdField()
    events = fields.Nested(EventsSchema)
    external_uid = fields.Str()
    external_name = fields.Str()
    product = fields.Nested(ProductSchema)
    connection = fields.Nested(ConnectionSchema)
    contract = fields.Nested(ContractSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    params = fields.Nested(ParamSchema, many=True)
    tiers = fields.Nested(TierAccountsSchema)
    items = fields.Nested(ItemSchema, many=True)
    configuration = fields.Nested(ConfigurationSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Asset
        return Asset(**data)


class AssigneeField(fields.Field):
    def _deserialize(self, value, attr=None, data=None):
        from connect.models.user import User
        if isinstance(value, six.string_types):
            return value
        else:
            return User.deserialize_json(value)


class AssetRequestSchema(BaseSchema):
    type = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    status = fields.Str()
    params_form_url = fields.Str()
    activation_key = fields.Str()
    reason = fields.Str()
    note = fields.Str()
    asset = fields.Nested(AssetSchema)
    contract = fields.Nested(ContractSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    assignee = AssigneeField()

    @post_load
    def make_object(self, data):
        from connect.models import AssetRequest
        return AssetRequest(**data)


class FulfillmentSchema(AssetRequestSchema):
    @deprecated(deprecated_in='19.2',
                details='Use `connect.models.schemas.AssetRequestSchema` instead.')
    def __init__(self, *args, **kwargs):
        super(FulfillmentSchema, self).__init__(*args, **kwargs)

    @post_load
    def make_object(self, data):
        from connect.models import Fulfillment
        return Fulfillment(**data)


class TierConfigSchema(BaseSchema):
    name = fields.Str()
    account = fields.Nested(TierAccountSchema)
    product = fields.Nested(ProductSchema)
    tier_level = fields.Int()
    params = fields.Nested(ParamSchema, many=True)
    connection = fields.Nested(ConnectionSchema)
    open_request = fields.Nested(BaseSchema)
    template = fields.Nested(TemplateSchema)
    contract = fields.Nested(ContractSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    configuration = fields.Nested(ConfigurationSchema)
    events = fields.Nested(EventsSchema)
    status = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import TierConfig
        return TierConfig(**data)


class TierConfigRequestSchema(BaseSchema):
    type = fields.Str()
    status = fields.Str()
    configuration = fields.Nested(TierConfigSchema)
    parent_configuration = fields.Nested(TierConfigSchema)
    account = fields.Nested(TierAccountSchema)
    product = fields.Nested(ProductSchema)
    tier_level = fields.Int()
    params = fields.Nested(ParamSchema, many=True)
    environment = fields.Str()
    assignee = fields.Nested(UserSchema)
    template = fields.Nested(TemplateSchema)
    reason = fields.Str()
    activation = fields.Nested(ActivationSchema)
    notes = fields.Str()
    events = fields.Nested(EventsSchema)
    tiers = fields.Nested(TierAccountsSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    contract = fields.Nested(ContractSchema)

    @post_load
    def make_object(self, data):
        from connect.models import TierConfigRequest
        return TierConfigRequest(**data)


class UsageRecordsSchema(BaseSchema):
    valid = fields.Int()
    invalid = fields.Int()
    closed = fields.Int()

    @post_load
    def make_object(self, data):
        from connect.models import UsageRecords
        return UsageRecords(**data)


class UsageStatsSchema(BaseSchema):
    uploaded = fields.Int()
    validated = fields.Int()
    pending = fields.Int()
    accepted = fields.Int()
    closed = fields.Int()
    invalid = fields.Int()

    @post_load
    def make_object(self, data):
        from connect.models import UsageStats
        return UsageStats(**data)


class UsageFileSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str()
    note = fields.Str()
    status = fields.Str()
    period_from = fields.Str()
    period_to = fields.Str()
    currency = fields.Str()
    schema = fields.Str()
    created_by = fields.Str()
    created_at = fields.Str()
    usage_file_uri = fields.Str()
    processed_file_uri = fields.Str()
    product = fields.Nested(ProductSchema)
    contract = fields.Nested(ContractSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    vendor = fields.Nested(CompanySchema)
    provider = fields.Nested(CompanySchema)
    acceptance_note = fields.Str()
    rejection_note = fields.Str()
    error_details = fields.Str()
    external_id = fields.Str()
    stats = fields.Nested(UsageStatsSchema)
    records = fields.Nested(UsageRecordsSchema)
    events = fields.Nested(EventsSchema)

    @post_load
    def make_object(self, data):
        from connect.models import UsageFile
        return UsageFile(**data)


class UsageListingSchema(BaseSchema):
    status = fields.Str()
    contract = fields.Nested(ContractSchema)
    product = fields.Nested(ProductSchema)
    created = fields.Str()

    # Undocumented fields (they appear in PHP SDK)
    vendor = fields.Nested(CompanySchema)
    provider = fields.Nested(CompanySchema)

    @post_load
    def make_object(self, data):
        from connect.models import UsageListing
        return UsageListing(**data)


class UsageRecordSchema(BaseSchema):
    usage_record_id = fields.Str()
    usage_record_note = fields.Str()
    item_search_criteria = fields.Str()
    item_search_value = fields.Str()
    amount = fields.Int()
    quantity = fields.Int()
    start_time_utc = fields.Str()
    end_time_utc = fields.Str()
    asset_search_criteria = fields.Str()
    asset_search_value = fields.Str()
    item_name = fields.Str()
    item_npm = fields.Str()
    item_unit = fields.Str()
    item_precision = fields.Str()
    category_id = fields.Str()
    asset_recon_id = fields.Str()
    tier = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import UsageRecord
        return UsageRecord(**data)


class ConversationMessageSchema(BaseSchema):
    conversation = fields.Str()
    created = fields.DateTime()
    creator = fields.Nested(UserSchema)
    text = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import ConversationMessage
        return ConversationMessage(**data)


class ConversationSchema(BaseSchema):
    instance_id = fields.Str()
    created = fields.DateTime()
    topic = fields.Str()
    messages = fields.Nested(ConversationMessageSchema, many=True)
    creator = fields.Nested(UserSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Conversation
        return Conversation(**data)


class AttributesSchema(BaseSchema):
    provider = fields.Nested(CompanySchema, only=('external_id',))
    vendor = fields.Nested(CompanySchema, only=('external_id',))

    @post_load
    def make_object(self, data):
        from connect.models import Attributes
        return Attributes(**data)


class AnniversarySchema(BaseSchema):
    day = fields.Integer()
    month = fields.Integer()

    @post_load
    def make_object(self, data):
        from connect.models import Anniversary
        return Anniversary(**data)


class StatSchema(BaseSchema):
    count = fields.Integer()
    last_request = fields.Nested(LastRequestSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Stat
        return Stat(**data)


class StatsSchema(BaseSchema):
    provider = fields.Nested(StatSchema)
    vendor = fields.Nested(StatSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Stats
        return Stats(**data)


class BillingSchema(BaseSchema):
    stats = fields.Nested(StatsSchema)
    period = fields.Nested(PeriodSchema)
    next_date = fields.DateTime()
    anniversary = fields.Nested(AnniversarySchema)

    @post_load
    def make_object(self, data):
        from connect.models import Billing
        return Billing(**data)


class BillingRequestSchema(BaseSchema):
    type = fields.String()
    events = fields.Nested(EventsSchema, only=('created', 'updated'))
    asset = fields.Nested(AssetSchema)
    items = fields.Nested(ItemSchema, many=True)
    attributes = fields.Nested(AttributesSchema)
    period = fields.Nested(PeriodSchema)

    @post_load
    def make_object(self, data):
        from connect.models import BillingRequest
        return BillingRequest(**data)


class RecurringAssetSchema(BaseSchema):
    id = fields.String()
    status = fields.String()
    events = fields.Nested(EventsSchema, only=('created', 'updated'))
    external_id = fields.String()
    external_uuid = fields.String()
    product = fields.Nested(ProductSchema, only=('id', 'name', 'status', 'icon'))
    connection = fields.Nested(ConnectionSchema)
    items = fields.Nested(ItemSchema, many=True)
    params = fields.Nested(ParamSchema, many=True)
    tiers = fields.Nested(TierAccountSchema)
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name', 'icon'))
    contract = fields.Nested(ContractSchema, only=('id', 'name'))
    billing = fields.Nested(BillingSchema)

    @post_load
    def make_object(self, data):
        from connect.models import RecurringAsset
        return RecurringAsset(**data)
