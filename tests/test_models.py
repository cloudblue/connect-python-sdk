# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json
import os
from collections import namedtuple

from mock import MagicMock, patch

from connect.config import Config
from connect.resource import FulfillmentResource

response = namedtuple('Response', ('ok', 'content'))


def _get_response_ok():
    response.ok = True
    with open(os.path.join(os.path.dirname(__file__), 'response.json')) as file_handle:
        response.content = file_handle.read()

    return response


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_model_from_response():
    config = Config(api_key='ApiKey XXXX:YYYYY', api_url='http://localhost:8080/api/public/v1/')

    requests = FulfillmentResource(config).list()
    request_obj = FulfillmentResource(config).get(pk='PR-000-000-000')

    assert requests[0].id == request_obj.id
    content = json.loads(response.content)[0]
    assert request_obj.id == content['id']
    assert request_obj.contract.id == content['contract']['id']
    assert request_obj.marketplace.id == content['marketplace']['id']
    assert request_obj.asset.id == content['asset']['id']
    assert request_obj.asset.product.id == content['asset']['product']['id']

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
