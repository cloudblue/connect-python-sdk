# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import json
import os
from collections import namedtuple

from mock import MagicMock, patch

from connect import TierConfigRequestAutomation

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
        content = json.loads(file_handle.read())

    # Get tier config request from response
    # resource = TierConfigRequestAutomation()
    # request = resource.list
