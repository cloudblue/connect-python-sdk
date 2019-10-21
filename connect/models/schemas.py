# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from marshmallow import Schema, fields, post_load
import six


class BaseSchema(Schema):
    id = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import BaseModel
        return BaseModel(**data)


class ActivationSchema(BaseSchema):
    link = fields.Str(allow_none=True)
    message = fields.Str()
    date = fields.DateTime(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Activation
        return Activation(**data)


class AgreementStatsSchema(BaseSchema):
    contracts = fields.Int(allow_none=True)
    versions = fields.Int()

    @post_load
    def make_object(self, data):
        from connect.models import AgreementStats
        return AgreementStats(**data)


class CompanySchema(BaseSchema):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Company
        return Company(**data)


class PhoneNumberSchema(BaseSchema):
    country_code = fields.Str(allow_none=True)
    area_code = fields.Str(allow_none=True)
    phone_number = fields.Str(allow_none=True)
    extension = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import PhoneNumber
        return PhoneNumber(**data)


class ContactSchema(BaseSchema):
    email = fields.Str()
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    phone_number = fields.Nested(PhoneNumberSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Contact
        return Contact(**data)


class ContactInfoSchema(BaseSchema):
    address_line1 = fields.Str()
    address_line2 = fields.Str(allow_none=True)
    city = fields.Str()
    contact = fields.Nested(ContactSchema)
    country = fields.Str()
    postal_code = fields.Str()
    state = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ContactInfo
        return ContactInfo(**data)


class ValueChoiceSchema(Schema):
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
    email = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import User
        return User(**data)


class EventSchema(BaseSchema):
    at = fields.DateTime(allow_none=True)
    by = fields.Nested(UserSchema, allow_none=True)

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
    description = fields.Str(allow_none=True)
    instance = fields.Nested(HubInstanceSchema)
    events = fields.Nested(EventsSchema)
    stats = fields.Nested(HubStatsSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Hub
        return Hub(**data)


class ExternalIdField(fields.Field):
    def _deserialize(self, value, attr, obj, **kwargs):
        if isinstance(value, six.string_types):
            return value
        elif isinstance(value, int):
            return str(value)
        else:
            raise ValueError({attr: [u'Not a valid int or string.']})


class ExtIdHubSchema(Schema):
    hub = fields.Nested(HubSchema, only=('id', 'name'))
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
    def _deserialize(self, value, attr, obj, **kwargs):
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
    owner = fields.Nested(CompanySchema, only=('id', 'name'))
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
    value = fields.Str(allow_none=True)
    value_error = fields.Str(allow_none=True)
    value_choice = fields.Str(many=True, allow_none=True)

    # Undocumented fields (they appear in PHP SDK)
    title = fields.Str(allow_none=True)
    scope = fields.Str(allow_none=True)
    constraints = fields.Nested(ConstraintsSchema, allow_none=True)
    value_choices = fields.Nested(ValueChoiceSchema, many=True, allow_none=True)
    phase = fields.Str(allow_none=True)
    events = fields.Nested(EventsSchema, allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, allow_none=True)
    countries = fields.Nested(CountrySchema, many=True, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Param
        return Param(**data)


class ItemSchema(BaseSchema):
    mpn = fields.Str()
    quantity = QuantityField()
    old_quantity = QuantityField(allow_none=True)
    renewal = fields.Nested(RenewalSchema, allow_none=True)
    params = fields.Nested(ParamSchema, many=True, allow_none=True)
    display_name = fields.Str(allow_none=True)
    global_id = fields.Str(allow_none=True)
    item_type = fields.Str(allow_none=True)
    period = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)
    name = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Item
        return Item(**data)


class AgreementSchema(BaseSchema):
    type = fields.Str()
    title = fields.Str()
    description = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    owner = fields.Nested(CompanySchema)
    stats = fields.Nested(AgreementStatsSchema, allow_none=True)
    author = fields.Nested(UserSchema, allow_none=True)
    version = fields.Int()
    active = fields.Bool()
    link = fields.Str()
    version_created = fields.DateTime()
    version_contracts = fields.Int()
    agreements = fields.Nested('AgreementSchema', many=True)
    parent = fields.Nested('AgreementSchema', only=('id', 'name'), allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'), allow_none=True)
    name = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Agreement
        return Agreement(**data)


class ContractSchema(BaseSchema):
    name = fields.Str()
    version = fields.Int()
    type = fields.Str()
    status = fields.Str()
    agreement = fields.Nested(AgreementSchema, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'), allow_none=True)
    owner = fields.Nested(CompanySchema, only=('id', 'name'), allow_none=True)
    creator = fields.Nested(UserSchema, only=('id', 'name'))
    created = fields.DateTime()
    updated = fields.DateTime()
    enrolled = fields.DateTime(allow_none=True)
    version_created = fields.DateTime()
    activation = fields.Nested(ActivationSchema)
    signee = fields.Nested(UserSchema, only=('id', 'name'), allow_none=True)

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
    parent = fields.Nested('ProductCategorySchema', allow_none=True)
    children = fields.Nested('ProductCategorySchema', many=True, allow_none=True)
    family = fields.Nested(ProductFamilySchema, allow_none=True)

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
    value = fields.Str(allow_none=True)
    parameter = fields.Nested(ParamSchema)
    marketplace = fields.Nested(MarketplaceSchema, allow_none=True)
    item = fields.Nested(ItemSchema, allow_none=True)
    events = fields.Nested(EventsSchema)
    constraints = fields.Nested(ConstraintsSchema, allow_none=True)

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
    published_at = fields.DateTime(allow_none=True)
    configurations = fields.Nested(ProductConfigurationSchema)
    customer_ui_settings = fields.Nested(CustomerUiSettingsSchema)
    category = fields.Nested(ProductCategorySchema, allow_none=True)
    owner = fields.Nested(CompanySchema, allow_none=True)
    latest = fields.Bool(allow_none=True)
    stats = fields.Nested(ProductStatsSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Product
        return Product(**data)


class ServerErrorResponseSchema(Schema):
    error_code = fields.Str()
    params = fields.Dict(allow_none=True)
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

    @post_load
    def make_object(self, data):
        from connect.models import TierAccount
        return TierAccount(**data)


class TierAccountsSchema(Schema):
    customer = fields.Nested(TierAccountSchema)
    tier1 = fields.Nested(TierAccountSchema, allow_none=True)
    tier2 = fields.Nested(TierAccountSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import TierAccounts
        return TierAccounts(**data)


class ConnectionSchema(BaseSchema):
    type = fields.Str()
    provider = fields.Nested(CompanySchema, only=('id', 'name'))
    vendor = fields.Nested(CompanySchema, only=('id', 'name'))
    product = fields.Nested(ProductSchema)
    hub = fields.Nested(HubSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Connection
        return Connection(**data)


class AssetSchema(BaseSchema):
    status = fields.Str()
    external_id = ExternalIdField()
    events = fields.Nested(EventsSchema, allow_none=True)
    external_uid = fields.Str(allow_none=True)
    external_name = fields.Str(allow_none=True)
    product = fields.Nested(ProductSchema, only=('id', 'name'))
    connection = fields.Nested(
        ConnectionSchema, only=('id', 'type', 'provider', 'vendor'),
    )
    contract = fields.Nested(ContractSchema, allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, allow_none=True)
    params = fields.Nested(ParamSchema, many=True)
    tiers = fields.Nested(TierAccountsSchema)
    items = fields.Nested(ItemSchema, many=True)
    configuration = fields.Nested(ConfigurationSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Asset
        return Asset(**data)


class AssigneeField(fields.Field):
    def _deserialize(self, value, attr, obj, **kwargs):
        from connect.models.user import User
        if isinstance(value, six.string_types):
            return value
        else:
            return User.deserialize_json(value)


class FulfillmentSchema(BaseSchema):
    type = fields.Str()
    created = fields.DateTime()
    updated = fields.DateTime()
    status = fields.Str()
    params_form_url = fields.Str()
    activation_key = fields.Str()
    reason = fields.Str()
    note = fields.Str()
    asset = fields.Nested(AssetSchema)
    contract = fields.Nested(ContractSchema, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'))
    assignee = AssigneeField(allow_none=True)

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
    open_request = fields.Nested(BaseSchema, allow_none=True)
    template = fields.Nested(TemplateSchema)
    contract = fields.Nested(ContractSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    configuration = fields.Nested(ConfigurationSchema, allow_none=True)
    events = fields.Nested(EventsSchema, allow_none=True)
    status = fields.Str(allow_none=True)

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
    assignee = fields.Nested(UserSchema, allow_none=True)
    template = fields.Nested(TemplateSchema, allow_none=True)
    reason = fields.Str(allow_none=True)
    activation = fields.Nested(ActivationSchema, allow_none=True)
    notes = fields.Str(allow_none=True)
    events = fields.Nested(EventsSchema, allow_none=True)
    tiers = fields.Nested(TierAccountsSchema, allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, allow_none=True)
    contract = fields.Nested(ContractSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import TierConfigRequest
        return TierConfigRequest(**data)


class UsageRecordsSchema(BaseSchema):
    valid = fields.Int()
    invalid = fields.Int()

    @post_load
    def make_object(self, data):
        from connect.models import UsageRecords
        return UsageRecords(**data)


class UsageFileSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str()
    note = fields.Str()
    status = fields.Str()
    created_by = fields.Str()
    created_at = fields.Str()
    upload_file_uri = fields.Str()
    processed_file_uri = fields.Str()
    product = fields.Nested(ProductSchema)
    contract = fields.Nested(ContractSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    vendor = fields.Nested(CompanySchema)
    provider = fields.Nested(CompanySchema)
    acceptance_note = fields.Str()
    rejection_note = fields.Str()
    error_details = fields.Str()
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
    item_search_criteria = fields.Str()
    item_search_value = fields.Str()
    quantity = fields.Int()
    start_time_utc = fields.Str()
    end_time_utc = fields.Str()
    asset_search_criteria = fields.Str()
    asset_search_value = fields.Str()

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
