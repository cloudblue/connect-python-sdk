# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json
import os
from collections import namedtuple

from mock import MagicMock, patch

from connect.models import Param
from connect.models.asset import Asset
from connect.models.fulfillment import Fulfillment
from connect.models.product import Item
from connect.resource import FulfillmentResource

Response = namedtuple('Response', ('ok', 'content'))


def _get_response_ok():
    with open(os.path.join(os.path.dirname(__file__), 'response.json')) as file_handle:
        content = file_handle.read()
    return Response(ok=True, content=content)


def _get_response2_ok():
    with open(os.path.join(os.path.dirname(__file__), 'response2.json')) as file_handle:
        content = file_handle.read()
    return Response(ok=True, content=content)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_model_from_response():
    # Parse JSON data from response file
    with open(os.path.join(os.path.dirname(__file__), 'response.json')) as file_handle:
        content = json.loads(file_handle.read())[0]

    # Get requests from response
    resource = FulfillmentResource()
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
        assert False, 'Incorrectly initialized model '

    # Assert that returned data matches the one in the file
    assert requests[0].id == request_obj.id
    assert request_obj.id == content['id']
    assert request_obj.contract.id == content['contract']['id']
    assert request_obj.marketplace.id == content['marketplace']['id']
    assert request_obj.asset.id == content['asset']['id']
    assert request_obj.asset.product.id == content['asset']['product']['id']
    try:
        # Python 2
        assert isinstance(request_obj.asset.external_id, basestring)
    except NameError:
        # Python 3
        assert isinstance(request_obj.asset.external_id, str)


@patch('requests.get', MagicMock(return_value=_get_response2_ok()))
def test_fulfillment_items():
    # Get request
    requests = FulfillmentResource().list()
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


@patch('requests.get', MagicMock(return_value=_get_response2_ok()))
def test_asset_methods():
    # Get asset
    requests = FulfillmentResource().list()
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
