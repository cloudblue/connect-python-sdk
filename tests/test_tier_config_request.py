# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import json
import os
from collections import namedtuple

import six
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
def test_create_model_from_response():
    # Parse JSON data from response file
    with open(os.path.join(os.path.dirname(__file__), 'response_tier_config_request.json'))\
            as file_handle:
        content = json.loads(file_handle.read())[0]

    # Get tier config request from response
    resource = TierConfigRequestAutomation()
    requests = resource.list
    assert isinstance(requests, list)
    assert len(requests) == 1
    request = requests[0]

    # Assert that fields are deserialized with the correct type
    assert isinstance(request, TierConfigRequest)
    assert isinstance(request.id, six.string_types)
    assert isinstance(request.type, six.string_types)
    assert isinstance(request.status, six.string_types)
    assert isinstance(request.configuration, TierConfig)
    assert isinstance(request.events, Events)
    assert isinstance(request.events.created, EventInfo)
    assert isinstance(request.events.created.at, six.string_types)
    assert not request.events.created.by
    assert isinstance(request.events.inquired, EventInfo)
    assert isinstance(request.events.inquired.at, six.string_types)
    assert isinstance(request.events.inquired.by, Company)
    assert isinstance(request.events.inquired.by.id, six.string_types)
    assert isinstance(request.events.inquired.by.name, six.string_types)
    assert isinstance(request.events.pended, EventInfo)
    assert isinstance(request.events.pended.at, six.string_types)
    assert isinstance(request.events.pended.by, Company)
    assert isinstance(request.events.pended.by.id, six.string_types)
    assert isinstance(request.events.pended.by.name, six.string_types)
    assert not request.events.validated
    assert not request.events.updated
    assert isinstance(request.params, list)
    for param in request.params:
        assert isinstance(param, Param)
    assert isinstance(request.assignee, Company)
    assert isinstance(request.template, Template)
    assert isinstance(request.activation, Activation)

    # Assert that data is parsed correctly
    assert request.id == content['id']
    assert request.type == content['type']
    assert request.status == content['status']
    assert not request.configuration.id
    assert request.events.created.at == content['events']['created']['at']
    assert request.events.inquired.at == content['events']['inquired']['at']
    assert request.events.inquired.by.id == content['events']['inquired']['by']['id']
    assert request.events.inquired.by.name == content['events']['inquired']['by']['name']
    assert request.events.pended.at == content['events']['pended']['at']
    assert request.events.pended.by.id == content['events']['pended']['by']['id']
    assert request.events.pended.by.name == content['events']['pended']['by']['name']
    assert len(request.params) == len(content['params'])
    for param_index in range(0, len(request.params)):
        assert request.params[param_index].id == content['params'][param_index]['id']
        assert request.params[param_index].value == content['params'][param_index]['value']
    assert request.assignee.id == content['assignee']['id']
    assert request.assignee.name == content['assignee']['name']
    assert request.template.id == content['template']['id']
    assert request.template.representation == content['template']['representation']
    assert request.activation.link == content['activation']['link']


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_get_tier_config():
    config = TierConfigRequestAutomation().get_tier_config(tier_id='', product_id='')
    assert isinstance(config, TierConfigRequest)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_get_tier_config_param():
    param = TierConfigRequestAutomation().get_tier_config_param(
        param_id='param_a',
        tier_id='',
        product_id='')
    assert isinstance(param, Param)
    assert param.id == 'param_a'
    assert param.value == 'param_a_value'
