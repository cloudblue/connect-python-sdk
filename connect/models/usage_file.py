# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .company import Company
from .contract import Contract
from .events import Events
from .marketplace import Marketplace
from .product import Product
from .usage_records import UsageRecords
from .usage_stats import UsageStats
from .schemas import UsageFileSchema


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

    period_from = None  # type: str
    """ (str) Date & time from which usage records are considered in this usage file. """

    period_to = None  # type: str
    """ (str) Date & time from which usage records are considered in this usage file. """

    currency = None  # type: str
    """ (str) Currency of the amount included in usage file. """

    schema = None  # type: str
    """ (str)Usage Scheme used for the usage file. """

    created_by = None  # type: str
    """ (str) User ID who have created this UsageFile. """

    created_at = None  # type: str
    """ (str) Date of the creation of the UsageFile. """

    usage_file_uri = None  # type: str
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
    # TODO: In the docs it is error_details, on PHP SDK it appears as error_detail

    external_id = None  # type: str
    """ (str) External ID of the file. """

    stats = None  # type: UsageStats
    """ (:py:class:`.UsageStats`) UsageStats Object. """

    records = None  # type: UsageRecords
    """ (:py:class:`.UsageRecords`) UsageRecords Object. """

    events = None  # type: Events
    """ (:py:class:`.Events`) Events occured on file. """

    environment = None  # type: str
    """ (str) Environment. """
