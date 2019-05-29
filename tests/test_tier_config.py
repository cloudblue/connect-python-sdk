# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import os
from datetime import datetime

import pytest
from mock import MagicMock, patch
from typing import Union

from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.models import Param, ActivationTileResponse, ActivationTemplateResponse, BaseModel, \
    Company, Connection, EventInfo, Hub, Product, TierConfigRequest, TierConfig, Events, \
    Template, Activation, User, TierAccount
from connect.resources import TierConfigAutomation
from .common import Response, load_str


def _get_response_ok():
    return Response(
        ok=True,
        text=load_str(os.path.join(
            os.path.dirname(__file__),
            'data',
            'response_tier_config_request.json')),
        status_code=200)


def _get_response_ok_invalid_product():
    response_ok = _get_response_ok()
    return Response(
        ok=response_ok.ok,
        text=response_ok.text.replace('CN-631-322-000', 'PRD-000-000-000'),
        status_code=response_ok.status_code)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_resource():
    requests = TierConfigAutomation().list()
    assert isinstance(requests, list)
    assert len(requests) == 1

    request = requests[0]
    assert isinstance(request, TierConfigRequest)
    assert request.id == 'TCR-000-000-000'
    assert request.type == 'setup'
    assert request.status == 'pending'

    configuration = request.configuration
    assert isinstance(configuration, TierConfig)
    assert configuration.id == 'TC-000-000-000'
    assert configuration.name == 'Configuration of Reseller'
    assert configuration.tier_level == 1

    account = configuration.account
    assert isinstance(account, TierAccount)
    assert account.id == 'TA-1-000-000-000'

    product = configuration.product
    assert isinstance(product, Product)
    assert product.id == 'CN-631-322-000'
    assert product.name == 'Product'

    connection = configuration.connection
    assert isinstance(connection, Connection)
    assert connection.id == 'CT-9861-7949-8492'
    assert connection.type == 'production'

    hub = connection.hub
    assert isinstance(hub, Hub)
    assert hub.id == 'HB-12345-12345'
    assert hub.name == 'Provider Production Hub'

    provider = connection.provider
    assert isinstance(provider, Company)
    assert provider.id == 'PA-9861-7949'
    assert provider.name == 'Ingram Micro Prod DA'

    vendor = connection.vendor
    assert isinstance(vendor, Company)
    assert vendor.id == 'VA-9861-7949'
    assert vendor.name == 'Large Largo and Co'

    events = configuration.events
    assert isinstance(events, Events)
    assert isinstance(events.created, EventInfo)
    assert isinstance(events.created.at, datetime)
    assert str(events.created.at) == '2018-11-21 11:10:29'
    assert not events.created.by
    assert not events.inquired
    assert not events.pended
    assert not events.validated
    assert isinstance(events.updated, EventInfo)
    assert isinstance(events.updated.at, datetime)
    assert str(events.updated.at) == '2018-11-21 11:10:29'
    assert isinstance(events.updated.by, User)
    assert events.updated.by.id == 'PA-000-000'
    assert events.updated.by.name == 'Username'

    params = configuration.params
    assert isinstance(params, list)
    assert len(request.params) == 1
    assert isinstance(request.params[0], Param)
    assert request.params[0].id == 'param_a'
    assert request.params[0].value == 'param_a_value'

    open_request = configuration.open_request
    assert isinstance(open_request, BaseModel)
    assert open_request.id == 'TCR-000-000-000'

    template = configuration.template
    assert isinstance(template, Template)
    assert template.id == 'TP-000-000-000'
    assert template.representation == 'Render text is here......'

    events = request.events
    assert isinstance(events, Events)
    assert isinstance(events.created, EventInfo)
    assert isinstance(events.created.at, datetime)
    assert str(events.created.at) == '2018-11-21 11:10:29'
    assert not events.created.by
    assert isinstance(events.inquired, EventInfo)
    assert isinstance(events.inquired.at, datetime)
    assert str(events.inquired.at) == '2018-11-21 11:10:29'
    assert isinstance(events.inquired.by, User)
    assert events.inquired.by.id == 'PA-000-000'
    assert events.inquired.by.name == 'Username'
    assert isinstance(events.pended, EventInfo)
    assert isinstance(events.pended.at, datetime)
    assert str(events.pended.at) == '2018-11-21 11:10:29'
    assert isinstance(events.pended.by, User)
    assert events.pended.by.id == 'PA-000-001'
    assert events.pended.by.name == 'Username1'
    assert not events.validated
    assert not events.updated

    params = request.params
    assert isinstance(params, list)
    assert len(request.params) == 1
    assert isinstance(request.params[0], Param)
    assert request.params[0].id == 'param_a'
    assert request.params[0].value == 'param_a_value'

    assignee = request.assignee
    assert isinstance(assignee, User)
    assert assignee.id == 'PA-000-000'
    assert assignee.name == 'Username'

    template = request.template
    assert isinstance(template, Template)
    assert template.id == 'TP-000-000-000'
    assert template.representation == 'Render text is here......'

    activation = request.activation
    assert isinstance(activation, Activation)
    assert activation.link == 'http://example.com'


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_process_no_result():
    automation = TierConfigAutomationHelper()
    automation.process()


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_process_not_implemented():
    with pytest.raises(NotImplementedError):
        automation = TierConfigAutomation()
        automation.process()


@patch('requests.get', MagicMock(return_value=_get_response_ok_invalid_product()))
def test_process_invalid_product():
    automation = TierConfigAutomationHelper()
    automation.process()


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
@patch('requests.post', MagicMock(return_value=_get_response_ok()))
def test_process_with_activation_tile():
    automation = TierConfigAutomationHelper(ActivationTileResponse())
    automation.process()


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
@patch('requests.post', MagicMock(return_value=_get_response_ok()))
def test_process_with_activation_template():
    automation = TierConfigAutomationHelper(ActivationTemplateResponse('TL-000-000-000'))
    automation.process()


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
@patch('requests.post', MagicMock(return_value=_get_response_ok()))
@patch('requests.put', MagicMock(return_value=_get_response_ok()))
def test_process_raise_inquire():
    automation = TierConfigAutomationHelper(exception_class=InquireRequest)
    automation.process()


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
@patch('requests.post', MagicMock(return_value=_get_response_ok()))
@patch('requests.put', MagicMock(return_value=_get_response_ok()))
def test_process_raise_fail():
    automation = TierConfigAutomationHelper(exception_class=FailRequest)
    automation.process()


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
@patch('requests.post', MagicMock(return_value=_get_response_ok()))
@patch('requests.put', MagicMock(return_value=_get_response_ok()))
def test_process_raise_skip():
    automation = TierConfigAutomationHelper(exception_class=SkipRequest)
    automation.process()


class TierConfigAutomationHelper(TierConfigAutomation):
    def __init__(self, response='', exception_class=None):
        # type: (Union[ActivationTemplateResponse, ActivationTileResponse, str], type) -> None
        super(TierConfigAutomationHelper, self).__init__()
        self.response = response
        self.exception_class = exception_class

    def process_request(self, request):
        if self.exception_class:
            raise self.exception_class(self.response)
        else:
            return self.response
