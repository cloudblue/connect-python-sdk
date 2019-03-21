# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import os
from collections import namedtuple

from mock import MagicMock, patch

from connect import TierConfigRequestAutomation
from connect.models import Param
from connect.models.company import Company
from connect.models.tier_config import TierConfigRequest, TierConfig, Events, Template, \
    Activation, EventInfo

Response = namedtuple('Response', ('ok', 'content'))


def _get_response_ok():
    with open(os.path.join(os.path.dirname(__file__), 'response_tier_config_request.json'))\
            as file_handle:
        content = file_handle.read()
    return Response(ok=True, content=content)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_resource():
    requests = TierConfigRequestAutomation().list
    assert isinstance(requests, list)
    assert len(requests) == 1

    request = requests[0]
    assert isinstance(request, TierConfigRequest)
    assert request.id == 'TCR-000-000-000'
    assert request.type == 'setup'
    assert request.status == 'pending'

    configuration = request.configuration
    assert isinstance(configuration, TierConfig)
    assert not configuration.id

    events = request.events
    assert isinstance(events, Events)
    assert isinstance(events.created, EventInfo)
    assert events.created.at == '2018-11-21T11:10:29+00:00'
    assert not events.created.by
    assert isinstance(events.inquired, EventInfo)
    assert events.inquired.at == '2018-11-21T11:10:29+00:00'
    assert isinstance(events.inquired.by, Company)
    assert events.inquired.by.id == 'PA-000-000'
    assert events.inquired.by.name == 'Username'
    assert isinstance(events.pended, EventInfo)
    assert events.pended.at == '2018-11-21T11:10:29+00:00'
    assert isinstance(events.pended.by, Company)
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
    assert isinstance(assignee, Company)
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
def test_get_tier_config():
    config = TierConfigRequestAutomation().get_tier_config(tier_id='', product_id='')
    assert isinstance(config, TierConfig)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_get_tier_config_param():
    param = TierConfigRequestAutomation().get_tier_config_param(
        param_id='param_a',
        tier_id='',
        product_id='')
    assert isinstance(param, Param)
    assert param.id == 'param_a'
    assert param.value == 'param_a_value'
