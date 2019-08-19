# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .company import Company
from .marketplace import Contract, Marketplace
from .product import Product
from connect.models.schemas import UsageRecordsSchema, UsageFileSchema, UsageListingSchema, \
    UsageRecordSchema


class UsageRecords(BaseModel):
    """ Usage Records Object. """
    # TODO: Verify that this data is correct.

    _schema = UsageRecordsSchema()

    valid = None  # type: int
    """ (int) Valid. """

    invalid = None  # type: int
    """ (int) Invalid. """


class UsageFile(BaseModel):
    """ Usage File Object. """

    _schema = UsageFileSchema()

    name = None  # type: str
    """ (str) Name of the Usage file object. """

    description = None  # type: str
    """ (str) Vendor can provide a description value in this field to describe
    the file content.
    """

    note = None  # type: str
    """ (str) Vendor can put a note which can be refer later for some extra information. """

    status = None  # type: str
    """ (str) One of: draft, uploading, uploaded, processing, invalid, ready, rejected,
    pending, accepted, closed.
    """

    created_by = None  # type: str
    """ (str) User ID who have created this UsageFile. """

    created_at = None  # type: str
    """ (str) Date of the creation of the UsageFile. """

    upload_file_uri = None  # type: str
    """ (str) Google Storage shared location of the upload file. Only available in GET API
    and not included in list API (sharing timeout 600 sec).
    """

    processed_file_uri = None  # type: str
    """ (str) Google Storage shared location of the generated file after processing uploaded file.
    Only available in GET API and not included in list API (sharing timeout 30 sec).
    """

    product = None  # type: Product
    """ (:py:class:`.Product`) Reference on Product Object. """

    contract = None  # type: Contract
    """ (:py:class:`.Contract`) Reference on Contract Object. """

    marketplace = None  # type: Marketplace
    """ (:py:class:`.Marketplace` Reference on Marketplace Object. """

    vendor = None  # type: Company
    """ (:py:class:`.Company` Reference object to the vendor company. """

    provider = None  # type: Company
    """ (:py:class:`.Company` Reference object to the provider company. """

    acceptance_note = None  # type: str
    """ (str) Note provided by the provider in case of acceptance of the usage file. """

    rejection_note = None  # type: str
    """(str) Note provider by the provider in case of rejection of the usage file. """

    error_details = None  # type: str
    """ (str) In case of invalid file, this field will contain errors related to the file. """

    records = None  # type: UsageRecords
    """ (:py:class:`.UsageRecords`) UsageRecords Object. """

    uploaded_by = None  # type: str
    """ (str) User Id who uploaded the file. """

    uploaded_at = None  # type: str
    """ (str) Usage file upload time. """

    submitted_by = None  # type: str
    """ (str) User Id, who submitted the usage record to Provider. """

    submitted_at = None  # type: str
    """ (str) User Id, who submitted the usage record to Provider. """

    accepted_by = None  # type: str
    """ (str) User Id, who accepted the usage file as provider. """

    accepted_at = None  # type: str
    """ (str) Usage file acceptance time. """

    rejected_by = None  # type: str
    """ (str) User Id, who rejected the usage file as provider. """

    rejected_at = None  # type: str
    """ (str) Usage file rejection time. """

    closed_by = None  # type: str
    """ (str) User Id, who billed the usage file as provider. """

    closed_at = None  # type: str
    """ (str) Usage file billing time. """


class UsageListing(BaseModel):
    """ Usage Listing Object. """

    _schema = UsageListingSchema()

    status = None  # type: str
    """ (str) Status. """

    contract = None  # type: Contract
    """ (:py:class:`.Contract`) Contract Object. """

    product = None  # type: Product
    """ (:py:class:`.Product`) Product Object. """

    created = None  # type: str
    """ (str) Creation time. """

    # Undocumented fields (they appear in PHP SDK)
    vendor = None  # type: Company
    """ (:py:class:`.Company`) Vendor Object. """

    provider = None  # type: Company
    """ (:py:class:`.Company`) Provider Object. """


class UsageRecord(BaseModel):
    """ Usage Record Object. """

    _schema = UsageRecordSchema()

    usage_record_id = None  # type: str
    """ (str) Usage record id. """

    item_search_criteria = None  # type: str
    """ (str) Item search criteria. """

    item_search_value = None  # type: str
    """ (str) Item search value. """

    quantity = None  # type: int
    """ (int) Quantity. """

    start_time_utc = None  # type: str
    """ (str) Start Time in UTC. """

    end_time_utc = None  # type: str
    """ (str) End Time in UTC. """

    asset_search_criteria = None  # type: str
    """ (str) Asset search criteria. """

    asset_search_value = None  # type: str
    """ (str) Asset search value. """
