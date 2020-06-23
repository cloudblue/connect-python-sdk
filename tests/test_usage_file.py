# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
from datetime import datetime

import pytest
from mock import patch, MagicMock

from connect.exceptions import AcceptUsageFile, CloseUsageFile, DeleteUsageFile, RejectUsageFile, \
    SkipRequest, SubmitUsageFile
from connect.models import Company, Contract, Marketplace, Product, UsageRecords, UsageFile, \
    UsageStats
from connect.resources import UsageFileAutomation
from .common import Response, load_str

current_action = ''


# noinspection PyUnusedLocal
def _get_response_ok(*args, **kwargs):
    text = load_str(os.path.join(os.path.dirname(__file__), 'data', 'response_usage_file.json'))
    if current_action:
        text = text.replace('UF-2018-11-9878764342',
                            'UF-2018-11-9878764342-' + current_action)
    return Response(ok=True, text=text, status_code=200)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_resource():
    requests = UsageFileAutomationTester().list()
    assert isinstance(requests, list)
    assert len(requests) == 1

    request = requests[0]
    assert isinstance(request, UsageFile)
    assert request.id == 'UF-2018-11-9878764342'
    assert request.name == 'Usage for Feb 2019'
    assert request.description == 'Usage for the product belonging to month Feb 2019'
    assert request.note == 'My personal note'
    assert request.status == 'READY'
    assert request.created_by == 'rahul.mondal@ingrammicro.com'
    assert request.created_at == '2018-11-21T11:10:29+00:00'

    product = request.product
    assert isinstance(product, Product)
    assert product.id == 'CN-631-322-000'
    assert product.name == 'Google Apps'
    assert product.icon == '/media/VA-587-127/CN-783-317-575/media/CN-783-317-575-logo.png'

    contract = request.contract
    assert isinstance(contract, Contract)
    assert contract.id == 'CRD-00000-00000-00000'
    assert contract.name == 'ACME Distribution Contract'

    marketplace = request.marketplace
    assert isinstance(marketplace, Marketplace)
    assert marketplace.id == 'MP-198987'
    assert marketplace.name == 'France'
    assert marketplace.icon == '/media/PA-123-123/marketplaces/MP-12345/image.png'

    vendor = request.vendor
    assert isinstance(vendor, Company)
    assert vendor.id == 'VA-587-127'
    assert vendor.name == 'Symantec'

    provider = request.provider
    assert isinstance(provider, Company)
    assert provider.id == 'PA-587-127'
    assert provider.name == 'ABC Corp'

    assert request.usage_file_uri == '<File Location for uploaded file>'
    assert request.processed_file_uri == '<File Location for generated file>'
    assert request.acceptance_note == 'All usage data is correct'
    assert request.rejection_note == 'Rejected due to wrong usage for item 56'
    assert request.error_details == 'Error details in case of usage file is marked as invalid'

    records = request.records
    assert isinstance(records, UsageRecords)
    stats = request.stats
    assert isinstance(stats, UsageStats)
    assert records.valid == 56
    assert records.invalid == 0

    assert request.events.uploaded.by.name == 'rahul.mondal@ingrammicro.com'
    assert request.events.uploaded.at == datetime(2018, 11, 21, 11, 10, 29)
    assert request.events.submitted.by.name == 'rahul.mondal@ingrammicro.com'
    assert request.events.submitted.at == datetime(2018, 11, 21, 11, 10, 29)
    assert request.events.accepted.by.name == 'admin@a1provider.com'
    assert request.events.accepted.at == datetime(2018, 11, 21, 11, 10, 29)
    assert request.events.rejected.by.name == 'admin@a1provider.com'
    assert request.events.rejected.at == datetime(2018, 11, 21, 11, 10, 29)
    assert request.events.closed.by.name == 'admin@a1provider.com'
    assert request.events.closed.at == datetime(2018, 11, 21, 11, 10, 29)


@patch('requests.get', MagicMock(side_effect=_get_response_ok))
@patch('requests.post', MagicMock())
def test_process():
    global current_action
    actions = ['accept', 'close', 'delete', 'reject', 'submit', 'skip']
    resource = UsageFileAutomationTester()

    # If process_request does not return an exception (as with default id), a UserWarning is raised
    with pytest.raises(UserWarning):
        resource.process()

    # Test that all other actions do not raise UserWarning
    for action in actions:
        current_action = action  # This is used by _get_response_ok to define request id
        resource.process()


class UsageFileAutomationTester(UsageFileAutomation):
    def process_request(self, request):
        # type: (UsageFile) -> None
        if request.id == 'UF-2018-11-9878764342-accept':
            raise AcceptUsageFile('Valid file moving forward')
        elif request.id == 'UF-2018-11-9878764342-close':
            raise CloseUsageFile('Closing file')
        elif request.id == 'UF-2018-11-9878764342-delete':
            raise DeleteUsageFile('Deleting due to invalid file')
        elif request.id == 'UF-2018-11-9878764342-reject':
            raise RejectUsageFile('Rejecting the file as a test')
        elif request.id == 'UF-2018-11-9878764342-submit':
            raise SubmitUsageFile()
        elif request.id == 'UF-2018-11-9878764342-skip':
            raise SkipRequest('Skipping')
