# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
import unittest

from mock import MagicMock, patch

from connect.config import Config
from connect.resources.tier_account_request_automation import (
    TierAccountRequestAction, TierAccountRequestAutomation)

from .common import Response, load_str

list_tier_account_request_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_list_tier_account_request.json'))
get_tier_account_request_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_get_tier_account_request.json'))


def _get_response_list():
    return Response(
        ok=True,
        text=list_tier_account_request_contents,
        status_code=200)


def _get_response_get():
    return Response(
        ok=True,
        text=get_tier_account_request_contents,
        status_code=200)


class MyExampleTARAutomation(TierAccountRequestAutomation):
    def process_request(self, request):
        if request.account.contact_info.country == 'ES':
            return TierAccountRequestAction(TierAccountRequestAction.ACCEPT)
        elif request.account.contact_info.country == 'IT':
            return TierAccountRequestAction(TierAccountRequestAction.IGNORE, 'No data')
        else:
            return TierAccountRequestAction(TierAccountRequestAction.SKIP)


class TestTierAccountRequestAutomation(unittest.TestCase):
    def setUp(self):
        self.config = Config(file='tests/config.json')

    @patch('requests.post')
    @patch('requests.get', MagicMock(return_value=_get_response_list()))
    def test_request_automation(self, post_mock):
        post_mock.return_value = _get_response_get()
        configuration = Config(file='examples/config.json')
        tier_account_example = MyExampleTARAutomation(config=configuration)
        tier_account_example.process()
        assert post_mock.call_count == 2
