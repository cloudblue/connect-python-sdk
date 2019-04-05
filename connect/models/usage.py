# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from marshmallow import fields, post_load

from connect.models.base import BaseModel, BaseSchema
from connect.models.company import Company, CompanySchema
from connect.models.marketplace import Contract, Marketplace, ContractSchema, MarketplaceSchema
from connect.models.product import Product, ProductSchema


class Records(BaseModel):
    valid = None  # type: int
    invalid = None  # type: int


class File(BaseModel):
    name = None  # type: str
    description = None  # type: str
    note = None  # type: str
    status = None  # type: str
    created_by = None  # type: str
    created_at = None  # type: str
    product = None  # type: Product
    contract = None  # type: Contract
    marketplace = None  # type: Marketplace
    vendor = None  # type: Company
    provider = None  # type: Company
    upload_file_uri = None  # type: str
    processed_file_uri = None  # type: str
    acceptance_note = None  # type: str
    rejection_note = None  # type: str
    error_detail = None  # type: str
    records = None  # type: Records
    uploaded_by = None  # type: str
    uploaded_at = None  # type: str
    submitted_by = None  # type: str
    submitted_at = None  # type: str
    accepted_by = None  # type: str
    accepted_at = None  # type: str
    rejected_by = None  # type: str
    rejected_at = None  # type: str
    closed_by = None  # type: str
    closed_at = None  # type: str


class Listing(BaseModel):
    status = None  # type: str
    contract = None  # type: Contract
    product = None  # type: Product
    created = None  # type: str

    # Undocumented fields (they appear in PHP SDK)
    vendor = None  # type: Company
    provider = None  # type: Company


class FileUsageRecord(BaseModel):
    record_id = None  # type: str
    item_search_criteria = None  # type: str
    item_search_value = None  # type: str
    quantity = None  # type: int
    start_time_utc = None  # type: str
    end_time_utc = None  # type: str
    asset_search_criteria = None  # type: str
    asset_search_value = None  # type: str


class RecordsSchema(BaseSchema):
    valid = fields.Int()
    invalid = fields.Int()

    @post_load
    def make_object(self, data):
        return Records(**data)


class FileSchema(BaseSchema):
    name = fields.Str()
    description = fields.Str()
    note = fields.Str()
    status = fields.Str()
    created_by = fields.Str()
    created_at = fields.Str()
    product = fields.Nested(ProductSchema)
    contract = fields.Nested(ContractSchema)
    marketplace = fields.Nested(MarketplaceSchema)
    vendor = fields.Nested(CompanySchema)
    provider = fields.Nested(CompanySchema)
    upload_file_uri = fields.Str()
    processed_file_uri = fields.Str()
    acceptance_note = fields.Str()
    rejection_note = fields.Str()
    error_detail = fields.Str()
    records = fields.Nested(RecordsSchema)
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
        return File(**data)


class ListingSchema(BaseSchema):
    status = fields.Str()
    contract = fields.Nested(ContractSchema)
    product = fields.Nested(ProductSchema)
    created = fields.Str()

    # Undocumented fields (they appear in PHP SDK)
    vendor = fields.Nested(CompanySchema)
    provider = fields.Nested(CompanySchema)

    @post_load
    def make_object(self, data):
        return Listing(**data)


class FileUsageRecordSchema(BaseSchema):
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
        return FileUsageRecord(**data)
