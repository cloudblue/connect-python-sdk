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
    message = fields.Str(allow_none=True)
    date = fields.DateTime(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Activation
        return Activation(**data)


class AgreementStatsSchema(BaseSchema):
    contracts = fields.Int(allow_none=True)
    versions = fields.Int(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import AgreementStats
        return AgreementStats(**data)


class CompanySchema(BaseSchema):
    name = fields.Str(allow_none=True)

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
    email = fields.Str(allow_none=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    phone_number = fields.Nested(PhoneNumberSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Contact
        return Contact(**data)


class ContactInfoSchema(BaseSchema):
    address_line1 = fields.Str(allow_none=True)
    address_line2 = fields.Str(allow_none=True)
    city = fields.Str(allow_none=True)
    contact = fields.Nested(ContactSchema, allow_none=True)
    country = fields.Str(allow_none=True)
    postal_code = fields.Str(allow_none=True)
    state = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ContactInfo
        return ContactInfo(**data)


class ValueChoiceSchema(Schema):
    value = fields.Str(allow_none=True)
    label = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ValueChoice
        return ValueChoice(**data)


class ConstraintsSchema(BaseSchema):
    hidden = fields.Bool(allow_none=True)
    required = fields.Bool(allow_none=True)
    choices = fields.Nested(ValueChoiceSchema, many=True, allow_none=True)
    unique = fields.Bool(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Constraints
        return Constraints(**data)


class DocumentSchema(BaseSchema):
    title = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Document
        return Document(**data)


class DownloadLinkSchema(BaseSchema):
    title = fields.Str(allow_none=True)
    url = fields.Str(allow_none=True)
    visible_for = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import DownloadLink
        return DownloadLink(**data)


class UserSchema(BaseSchema):
    name = fields.Str(allow_none=True)
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
    created = fields.Nested(EventSchema, allow_none=True)
    inquired = fields.Nested(EventSchema, allow_none=True)
    pended = fields.Nested(EventSchema, allow_none=True)
    validated = fields.Nested(EventSchema, allow_none=True)
    updated = fields.Nested(EventSchema, allow_none=True)
    approved = fields.Nested(EventSchema, allow_none=True)
    uploaded = fields.Nested(EventSchema, allow_none=True)
    submitted = fields.Nested(EventSchema, allow_none=True)
    accepted = fields.Nested(EventSchema, allow_none=True)
    rejected = fields.Nested(EventSchema, allow_none=True)
    closed = fields.Nested(EventSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Events
        return Events(**data)


class HubInstanceSchema(BaseSchema):
    type = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import HubInstance
        return HubInstance(**data)


class HubStatsSchema(BaseSchema):
    connections = fields.Int(allow_none=True)
    marketplaces = fields.Int(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import HubStats
        return HubStats(**data)


class HubSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    company = fields.Nested(CompanySchema, allow_none=True)
    description = fields.Str(allow_none=True)
    instance = fields.Nested(HubInstanceSchema, allow_none=True)
    events = fields.Nested(EventsSchema, allow_none=True)
    stats = fields.Nested(HubStatsSchema, allow_none=True)

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
    hub = fields.Nested(HubSchema, only=('id', 'name'), allow_none=True)
    external_id = ExternalIdField(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ExtIdHub
        return ExtIdHub(**data)


class RenewalSchema(BaseSchema):
    from_ = fields.DateTime(load_from='from', allow_none=True)
    to = fields.DateTime(allow_none=True)
    period_delta = fields.Int(allow_none=True)
    period_uom = fields.Str(allow_none=True)

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
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    active_contracts = fields.Int(allow_none=True)
    icon = fields.Str(allow_none=True)
    owner = fields.Nested(CompanySchema, only=('id', 'name'), allow_none=True)
    hubs = fields.Nested(ExtIdHubSchema, many=True, allow_none=True)
    zone = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Marketplace
        return Marketplace(**data)


class CountrySchema(BaseSchema):
    name = fields.Str(allow_none=True)
    icon = fields.Str(allow_none=True)
    zone = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Country
        return Country(**data)


class ParamSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    type = fields.Str(allow_none=True)
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
    mpn = fields.Str(allow_none=True)
    quantity = QuantityField(allow_none=True)
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
    type = fields.Str(allow_none=True)
    title = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    created = fields.DateTime(allow_none=True)
    updated = fields.DateTime(allow_none=True)
    owner = fields.Nested(CompanySchema, allow_none=True)
    stats = fields.Nested(AgreementStatsSchema, allow_none=True)
    author = fields.Nested(UserSchema, allow_none=True)
    version = fields.Int(allow_none=True)
    active = fields.Bool(allow_none=True)
    link = fields.Str(allow_none=True)
    version_created = fields.DateTime(allow_none=True)
    version_contracts = fields.Int(allow_none=True)
    agreements = fields.Nested('AgreementSchema', many=True, allow_none=True)
    parent = fields.Nested('AgreementSchema', only=('id', 'name'), allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'), allow_none=True)
    name = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Agreement
        return Agreement(**data)


class ContractSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    version = fields.Int(allow_none=True)
    type = fields.Str(allow_none=True)
    status = fields.Str(allow_none=True)
    agreement = fields.Nested(AgreementSchema, only=('id', 'name'), allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'), allow_none=True)
    owner = fields.Nested(CompanySchema, only=('id', 'name'), allow_none=True)
    creator = fields.Nested(UserSchema, only=('id', 'name'), allow_none=True)
    created = fields.DateTime(allow_none=True)
    updated = fields.DateTime(allow_none=True)
    enrolled = fields.DateTime(allow_none=True)
    version_created = fields.DateTime(allow_none=True)
    activation = fields.Nested(ActivationSchema, allow_none=True)
    signee = fields.Nested(UserSchema, only=('id', 'name'), allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Contract
        return Contract(**data)


class ProductConfigurationSchema(BaseSchema):
    suspend_resume_supported = fields.Bool(allow_none=True)
    requires_reseller_information = fields.Bool(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ProductConfiguration
        return ProductConfiguration(**data)


class CustomerUiSettingsSchema(BaseSchema):
    description = fields.Str(allow_none=True)
    getting_started = fields.Str(allow_none=True)
    download_links = fields.Nested(DownloadLinkSchema, many=True, allow_none=True)
    documents = fields.Nested(DocumentSchema, many=True, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import CustomerUiSettings
        return CustomerUiSettings(**data)


class ProductFamilySchema(BaseSchema):
    name = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ProductFamily
        return ProductFamily(**data)


class ProductCategorySchema(BaseSchema):
    name = fields.Str(allow_none=True)
    parent = fields.Nested('ProductCategorySchema', allow_none=True)
    children = fields.Nested('ProductCategorySchema', many=True, allow_none=True)
    family = fields.Nested(ProductFamilySchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ProductCategory
        return ProductCategory(**data)


class ProductStatsInfoSchema(BaseSchema):
    distribution = fields.Int(allow_none=True)
    sourcing = fields.Int(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ProductStatsInfo
        return ProductStatsInfo(**data)


class ProductStatsSchema(BaseSchema):
    listing = fields.Int(allow_none=True)
    agreements = fields.Nested(ProductStatsInfoSchema, allow_none=True)
    contracts = fields.Nested(ProductStatsInfoSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ProductStats
        return ProductStats(**data)


class ProductConfigurationParameterSchema(BaseSchema):
    value = fields.Str(allow_none=True)
    parameter = fields.Nested(ParamSchema, allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, allow_none=True)
    item = fields.Nested(ItemSchema, allow_none=True)
    events = fields.Nested(EventsSchema, allow_none=True)
    constraints = fields.Nested(ConstraintsSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ProductConfigurationParameter
        return ProductConfigurationParameter(**data)


class ProductSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    icon = fields.Str(allow_none=True)
    short_description = fields.Str(allow_none=True)
    detailed_description = fields.Str(allow_none=True)
    version = fields.Int(allow_none=True)
    published_at = fields.DateTime(allow_none=True)
    configurations = fields.Nested(ProductConfigurationSchema, allow_none=True)
    customer_ui_settings = fields.Nested(CustomerUiSettingsSchema, allow_none=True)
    category = fields.Nested(ProductCategorySchema, allow_none=True)
    owner = fields.Nested(CompanySchema, allow_none=True)
    latest = fields.Bool(allow_none=True)
    stats = fields.Nested(ProductStatsSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Product
        return Product(**data)


class ServerErrorResponseSchema(Schema):
    error_code = fields.Str(allow_none=True)
    params = fields.Dict(allow_none=True)
    errors = fields.Str(many=True, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ServerErrorResponse
        return ServerErrorResponse(**data)


class TemplateSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    representation = fields.Str(allow_none=True)
    body = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Template
        return Template(**data)


class ConfigurationSchema(BaseSchema):
    params = fields.Nested(ParamSchema, many=True, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Configuration
        return Configuration(**data)


class TierAccountSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    contact_info = fields.Nested(ContactInfoSchema, allow_none=True)
    external_id = ExternalIdField(allow_none=True)
    external_uid = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import TierAccount
        return TierAccount(**data)


class TierAccountsSchema(Schema):
    customer = fields.Nested(TierAccountSchema, allow_none=True)
    tier1 = fields.Nested(TierAccountSchema, allow_none=True)
    tier2 = fields.Nested(TierAccountSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import TierAccounts
        return TierAccounts(**data)


class ConnectionSchema(BaseSchema):
    type = fields.Str(allow_none=True)
    provider = fields.Nested(CompanySchema, only=('id', 'name'), allow_none=True)
    vendor = fields.Nested(CompanySchema, only=('id', 'name'), allow_none=True)
    product = fields.Nested(ProductSchema, allow_none=True)
    hub = fields.Nested(HubSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Connection
        return Connection(**data)


class AssetSchema(BaseSchema):
    status = fields.Str(allow_none=True)
    external_id = ExternalIdField(allow_none=True)
    events = fields.Nested(EventsSchema, allow_none=True)
    external_uid = fields.Str(allow_none=True)
    external_name = fields.Str(allow_none=True)
    product = fields.Nested(ProductSchema, only=('id', 'name'), allow_none=True)
    connection = fields.Nested(
        ConnectionSchema, only=('id', 'type', 'provider', 'vendor'), allow_none=True
    )
    contract = fields.Nested(ContractSchema, allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, allow_none=True)
    params = fields.Nested(ParamSchema, many=True, allow_none=True)
    tiers = fields.Nested(TierAccountsSchema, allow_none=True)
    items = fields.Nested(ItemSchema, many=True, allow_none=True)
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
    type = fields.Str(allow_none=True)
    created = fields.DateTime(allow_none=True)
    updated = fields.DateTime(allow_none=True)
    status = fields.Str(allow_none=True)
    params_form_url = fields.Str(allow_none=True)
    activation_key = fields.Str(allow_none=True)
    reason = fields.Str(allow_none=True)
    note = fields.Str(allow_none=True)
    asset = fields.Nested(AssetSchema, allow_none=True)
    contract = fields.Nested(ContractSchema, only=('id', 'name'), allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'), allow_none=True)
    assignee = AssigneeField(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Fulfillment
        return Fulfillment(**data)


class TierConfigSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    account = fields.Nested(TierAccountSchema, allow_none=True)
    product = fields.Nested(ProductSchema, allow_none=True)
    tier_level = fields.Int(allow_none=True)
    params = fields.Nested(ParamSchema, many=True, allow_none=True)
    connection = fields.Nested(ConnectionSchema, allow_none=True)
    open_request = fields.Nested(BaseSchema, allow_none=True)
    template = fields.Nested(TemplateSchema, allow_none=True)
    contract = fields.Nested(ContractSchema, allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, allow_none=True)
    configuration = fields.Nested(ConfigurationSchema, allow_none=True)
    events = fields.Nested(EventsSchema, allow_none=True)
    status = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import TierConfig
        return TierConfig(**data)


class TierConfigRequestSchema(BaseSchema):
    type = fields.Str(allow_none=True)
    status = fields.Str(allow_none=True)
    configuration = fields.Nested(TierConfigSchema, allow_none=True)
    parent_configuration = fields.Nested(TierConfigSchema, allow_none=True)
    account = fields.Nested(TierAccountSchema, allow_none=True)
    product = fields.Nested(ProductSchema, allow_none=True)
    tier_level = fields.Int(allow_none=True)
    params = fields.Nested(ParamSchema, many=True, allow_none=True)
    environment = fields.Str(allow_none=True)
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
    valid = fields.Int(allow_none=True)
    invalid = fields.Int(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import UsageRecords
        return UsageRecords(**data)


class UsageFileSchema(BaseSchema):
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    note = fields.Str(allow_none=True)
    status = fields.Str(allow_none=True)
    created_by = fields.Str(allow_none=True)
    created_at = fields.Str(allow_none=True)
    upload_file_uri = fields.Str(allow_none=True)
    processed_file_uri = fields.Str(allow_none=True)
    product = fields.Nested(ProductSchema, allow_none=True)
    contract = fields.Nested(ContractSchema, allow_none=True)
    marketplace = fields.Nested(MarketplaceSchema, allow_none=True)
    vendor = fields.Nested(CompanySchema, allow_none=True)
    provider = fields.Nested(CompanySchema, allow_none=True)
    acceptance_note = fields.Str(allow_none=True)
    rejection_note = fields.Str(allow_none=True)
    error_details = fields.Str(allow_none=True)
    records = fields.Nested(UsageRecordsSchema, allow_none=True)
    events = fields.Nested(EventsSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import UsageFile
        return UsageFile(**data)


class UsageListingSchema(BaseSchema):
    status = fields.Str(allow_none=True)
    contract = fields.Nested(ContractSchema, allow_none=True)
    product = fields.Nested(ProductSchema, allow_none=True)
    created = fields.Str(allow_none=True)

    # Undocumented fields (they appear in PHP SDK)
    vendor = fields.Nested(CompanySchema, allow_none=True)
    provider = fields.Nested(CompanySchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import UsageListing
        return UsageListing(**data)


class UsageRecordSchema(BaseSchema):
    usage_record_id = fields.Str(allow_none=True)
    item_search_criteria = fields.Str(allow_none=True)
    item_search_value = fields.Str(allow_none=True)
    quantity = fields.Int(allow_none=True)
    start_time_utc = fields.Str(allow_none=True)
    end_time_utc = fields.Str(allow_none=True)
    asset_search_criteria = fields.Str(allow_none=True)
    asset_search_value = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import UsageRecord
        return UsageRecord(**data)


class ConversationMessageSchema(BaseSchema):
    conversation = fields.Str(allow_none=True)
    created = fields.DateTime(allow_none=True)
    creator = fields.Nested(UserSchema, allow_none=True)
    text = fields.Str(allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import ConversationMessage
        return ConversationMessage(**data)


class ConversationSchema(BaseSchema):
    instance_id = fields.Str(allow_none=True)
    created = fields.DateTime(allow_none=True)
    topic = fields.Str(allow_none=True)
    messages = fields.Nested(ConversationMessageSchema, many=True, allow_none=True)
    creator = fields.Nested(UserSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import Conversation
        return Conversation(**data)
