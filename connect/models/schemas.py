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
    state = fields.Str()

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

    @post_load
    def make_object(self, data):
        from connect.models import Constraints
        return Constraints(**data)


class DocumentSchema(BaseSchema):
    title = fields.Str()
    url = fields.Str()
    visible_for = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Document
        return Document(**data)


class DownloadLinkSchema(BaseSchema):
    title = fields.Str()
    url = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import DownloadLink
        return DownloadLink(**data)


class UserSchema(BaseSchema):
    name = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import User
        return User(**data)


class EventInfoSchema(BaseSchema):
    at = fields.DateTime(allow_none=True)
    by = fields.Nested(UserSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import EventInfo
        return EventInfo(**data)


class EventsSchema(BaseSchema):
    created = fields.Nested(EventInfoSchema)
    inquired = fields.Nested(EventInfoSchema)
    pended = fields.Nested(EventInfoSchema)
    validated = fields.Nested(EventInfoSchema)
    updated = fields.Nested(EventInfoSchema)

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


class ExtIdHubSchema(Schema):
    hub = fields.Nested(HubSchema, only=('id', 'name'))
    external_id = fields.Str()

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


class ItemSchema(BaseSchema):
    mpn = fields.Str()
    quantity = QuantityField()
    old_quantity = QuantityField(allow_none=True)
    renewal = fields.Nested(RenewalSchema, allow_none=True)
    global_id = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Item
        return Item(**data)


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

    @post_load
    def make_object(self, data):
        from connect.models import Param
        return Param(**data)


class ProductSchema(BaseSchema):
    name = fields.Str()
    icon = fields.Str()
    short_description = fields.Str()
    detailed_description = fields.Str()
    version = fields.Int()
    configurations = fields.Nested(ProductConfigurationSchema)
    customer_ui_settings = fields.Nested(CustomerUiSettingsSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Product
        return Product(**data)


class ServerErrorResponseSchema(Schema):
    error_code = fields.Str()
    params = fields.Dict()
    errors = fields.List(fields.Str())

    @post_load
    def make_object(self, data):
        from connect.models import ServerErrorResponse
        return ServerErrorResponse(**data)


class TemplateSchema(BaseSchema):
    representation = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import Template
        return Template(**data)


class TierAccountSchema(BaseSchema):
    name = fields.Str()
    contact_info = fields.Nested(ContactInfoSchema)
    external_id = fields.Str()
    external_uid = fields.Str()

    @post_load
    def make_object(self, data):
        from connect.models import TierAccount
        return TierAccount(**data)


class TierAccountsSchema(Schema):
    customer = fields.Nested(TierAccountSchema)
    tier1 = fields.Nested(TierAccountSchema)
    tier2 = fields.Nested(TierAccountSchema)

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
    external_id = fields.Str()
    external_uid = fields.Str(allow_none=True)
    product = fields.Nested(ProductSchema, only=('id', 'name'))
    connection = fields.Nested(
        ConnectionSchema, only=('id', 'type', 'provider', 'vendor'),
    )
    items = fields.Nested(ItemSchema, many=True)
    params = fields.Nested(ParamSchema, many=True)
    tiers = fields.Nested(TierAccountsSchema)

    @post_load
    def make_object(self, data):
        from connect.models import Asset
        return Asset(**data)


class FulfillmentSchema(BaseSchema):
    activation_key = fields.Str()
    asset = fields.Nested(AssetSchema)
    status = fields.Str()
    type = fields.Str()
    updated = fields.DateTime()
    created = fields.DateTime()
    reason = fields.Str()
    note = fields.Str()
    params_form_url = fields.Str()
    contract = fields.Nested(ContractSchema, only=('id', 'name'))
    marketplace = fields.Nested(MarketplaceSchema, only=('id', 'name'))

    @post_load
    def make_object(self, data):
        from connect.models import Fulfillment
        return Fulfillment(**data)


class TierConfigSchema(BaseSchema):
    name = fields.Str()
    account = fields.Nested(TierAccountSchema)
    product = fields.Nested(ProductSchema)
    tier_level = fields.Int()
    connection = fields.Nested(ConnectionSchema)
    events = fields.Nested(EventsSchema, allow_none=True)
    params = fields.Nested(ParamSchema, many=True)
    template = fields.Nested(TemplateSchema)
    open_request = fields.Nested(BaseSchema, allow_none=True)

    @post_load
    def make_object(self, data):
        from connect.models import TierConfig
        return TierConfig(**data)


class TierConfigRequestSchema(BaseSchema):
    type = fields.Str()
    status = fields.Str()
    configuration = fields.Nested(TierConfigSchema)
    events = fields.Nested(EventsSchema, allow_none=True)
    params = fields.Nested(ParamSchema, many=True)
    assignee = fields.Nested(UserSchema, allow_none=True)
    template = fields.Nested(TemplateSchema, allow_none=True)
    reason = fields.Str(allow_none=True)
    activation = fields.Nested(ActivationSchema, allow_none=True)
    notes = fields.Str(allow_none=True)

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
    uploaded_by = fields.Str()
    uploaded_at = fields.Str()
    submitted_by = fields.Str()
    submitted_at = fields.Str()
    accepted_by = fields.Str()
    accepted_at = fields.Str()
    rejected_by = fields.Str()
    rejected_at = fields.Str()
    closed_by = fields.Str()
    closed_at = fields.Str()

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
    record_id = fields.Str()
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
