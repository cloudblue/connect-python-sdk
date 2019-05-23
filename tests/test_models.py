# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json
import os

import six
from mock import MagicMock, patch

from connect import FulfillmentAutomation
from connect.models import Param
from connect.models.asset import Asset
from connect.models.fulfillment import Fulfillment
from connect.models.product import Item
from connect.models.tier_config import TierConfig
from .common import Response, load_str


def _get_response_ok():
    return Response(
        ok=True,
        content=load_str(os.path.join(os.path.dirname(__file__), 'data', 'response.json')),
        status_code=200)


def _get_response_ok2():
    return Response(
        ok=True,
        content=load_str(os.path.join(os.path.dirname(__file__), 'data', 'response2.json')),
        status_code=200)


def _get_response_tier_config_ok():
    return Response(ok=True,
                    content=load_str(os.path.join(
                        os.path.dirname(__file__),
                        'data',
                        'response_tier_config_request.json')),
                    status_code=200)


def _get_response_migration():
    return Response(
        ok=True,
        content=load_str(os.path.join(
            os.path.dirname(__file__),
            'data',
            'response_migration.json')),
        status_code=200)


def test_resource_url():
    resource = FulfillmentAutomation()
    assert resource._api.get_url() == resource.config.api_url + resource.resource + '/'


def test_resource_urljoin():
    resource = FulfillmentAutomation()
    assert resource._api.base_path == resource.resource
    assert resource._api.get_url('hello/world') == '{}{}/hello/world' \
        .format(resource.config.api_url, resource.resource)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_model_from_response():
    # Parse JSON data from response file
    content = json.loads(_get_response_ok().content)[0]

    # Get requests from response
    resource = FulfillmentAutomation()
    requests = resource.list()
    request_obj = resource.get(pk='PR-000-000-000')

    # Assert that all properties exist
    try:
        (
            request_obj.contract,
            request_obj.contract.id,
            request_obj.marketplace,
            request_obj.marketplace.id,
            request_obj.type,
            request_obj.updated,
            request_obj.created,
            request_obj.reason,
            request_obj.activation_key,
            request_obj.status,
            request_obj.asset.external_id,
            request_obj.asset.external_uid,
            request_obj.asset.product,
            request_obj.asset.product.id,
            request_obj.asset.connection,
            request_obj.asset.items,
            request_obj.asset.params,
            request_obj.asset.tiers,
        )
    except AttributeError:
        assert False, 'Incorrectly initialized model'

    # Assert that returned data matches the one in the file
    assert requests[0].id == request_obj.id
    assert request_obj.id == content['id']
    assert request_obj.contract.id == content['contract']['id']
    assert request_obj.marketplace.id == content['marketplace']['id']
    assert request_obj.asset.id == content['asset']['id']
    assert request_obj.asset.product.id == content['asset']['product']['id']
    assert isinstance(request_obj.asset.external_id, six.string_types)


@patch('requests.get', MagicMock(return_value=_get_response_ok2()))
def test_fulfillment_items():
    # Get request
    requests = FulfillmentAutomation().list()
    assert isinstance(requests, list)
    assert len(requests) == 1
    request = requests[0]
    assert isinstance(request, Fulfillment)

    # Test new items
    new_items = request.new_items
    assert isinstance(new_items, list)
    assert len(new_items) == 2
    for item in new_items:
        assert isinstance(item, Item)

    # Test changed items
    changed_items = request.changed_items
    assert isinstance(new_items, list)
    assert len(changed_items) == 2
    for item in changed_items:
        assert isinstance(item, Item)

    # Test removed items
    removed_items = request.removed_items
    assert isinstance(removed_items, list)
    assert len(removed_items) == 1
    for item in removed_items:
        assert isinstance(item, Item)


@patch('requests.get', MagicMock(return_value=_get_response_ok2()))
def test_asset_methods():
    # Get asset
    requests = FulfillmentAutomation().list()
    assert len(requests) == 1
    assert isinstance(requests[0], Fulfillment)
    asset = requests[0].asset
    assert isinstance(asset, Asset)

    # Get param by id
    assert isinstance(asset.get_param_by_id('howyoufeel'), Param)
    assert asset.get_param_by_id('howyoufeel').id == 'howyoufeel'
    assert not asset.get_param_by_id('invalid-id')

    # Get item by id
    assert isinstance(asset.get_item_by_mpn('TEAM-ST3L2T1Y'), Item)
    assert asset.get_item_by_mpn('TEAM-ST3L2T1Y').mpn == 'TEAM-ST3L2T1Y'
    assert not asset.get_item_by_mpn('invalid-mpn')


@patch('requests.get')
def test_get_tier_config(get_mock):
    get_mock.return_value = _get_response_tier_config_ok()
    config = FulfillmentAutomation().get_tier_config('tier_id', 'product_id')
    assert isinstance(config, TierConfig)
    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/tier/config-requests',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'ApiKey XXXX:YYYYY'},
        params={
            'status': 'approved',
            'configuration__product__id': 'product_id',
            'configuration__account__id': 'tier_id'})


@patch('requests.get', MagicMock(return_value=Response(ok=True, content='[]', status_code=200)))
def test_get_tier_config_empty():
    config = FulfillmentAutomation().get_tier_config('', '')
    assert not config


@patch('requests.get', MagicMock(return_value=_get_response_tier_config_ok()))
def test_get_tier_config_param():
    tier_config = FulfillmentAutomation().get_tier_config('', '')
    param = tier_config.get_param_by_id('param_a')
    assert isinstance(param, Param)
    assert param.id == 'param_a'
    assert param.value == 'param_a_value'


@patch('requests.get', MagicMock(return_value=_get_response_ok2()))
def test_doesnt_need_migration():
    requests = FulfillmentAutomation().list()
    assert len(requests) == 1
    request = requests[0]
    assert isinstance(request, Fulfillment)
    assert not request.needs_migration()


@patch('requests.get', MagicMock(return_value=_get_response_migration()))
def test_needs_migration():
    requests = FulfillmentAutomation().list()
    assert len(requests) == 1
    request = requests[0]
    assert isinstance(request, Fulfillment)
    assert request.needs_migration()
