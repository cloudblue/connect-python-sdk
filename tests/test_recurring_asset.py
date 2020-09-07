# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
import unittest
from mock import patch, call, Mock
from connect.models import RecurringAsset
from connect.resources.subscription import RecurringAssetResource
from connect.config import Config
from .common import Response, load_str

get_recurring_asset_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_get_recurring_asset.json'))
list_recurring_asset_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_list_recurring_asset.json'))


class TestRecurringAsset(unittest.TestCase):
    def setUp(self):
        self.config = Config(file='tests/config.json')

    @patch('requests.get')
    def test_get_recurring_asset_ok(self, get_mock):
        # type: (Mock) -> None
        get_mock.side_effect = [
            Response(True, '[' + get_recurring_asset_contents + ']', 200),
            Response(True, get_recurring_asset_contents, 200)
        ]

        request = RecurringAssetResource(config=self.config)
        recurring_asset = request.get('AS-3110-7077-0368')
        assert get_mock.call_count == 1
        self.assertEqual(recurring_asset.external_id, 'BSM4FJZ7U3', msg=None)
        # 054922da-ceae-47de-8e5d-7a2950acbfe1
        get_mock.assert_has_calls([
            call(
                headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
                timeout=300,
                url='http://localhost:8080/api/public/v1/subscriptions/assets/AS-3110-7077-0368')
        ])
        assert isinstance(recurring_asset, RecurringAsset)

    @patch('requests.get')
    def test_get_recurring_asset_empty(self, get_mock):
        # type: (Mock) -> None
        get_mock.return_value = Response(True, '[]', 200)

        request = RecurringAssetResource(config=self.config)
        recurring_asset = request.get('AS-0000-0000-0000')
        assert get_mock.call_count == 1

        get_mock.assert_has_calls([
            call(
                headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
                timeout=300,
                url='http://localhost:8080/api/public/v1/subscriptions/assets/AS-0000-0000-0000')
        ])
        self.assertEqual(recurring_asset, [], msg=None)

    @patch('requests.get')
    def test_list_recurring_asset_ok(self, get_mock):
        # type: (Mock) -> None
        get_mock.side_effect = [
            Response(True, list_recurring_asset_contents, 200),
            Response(True, list_recurring_asset_contents, 200)
        ]

        request = RecurringAssetResource(config=self.config)
        recurring_asset = request.list()
        assert get_mock.call_count == 1

        get_mock.assert_has_calls([
            call(
                headers={'Authorization': 'ApiKey XXXX:YYYYY', 'Content-Type': 'application/json'},
                timeout=300,
                url='http://localhost:8080/api/public/v1/subscriptions/assets?limit=100')
        ])
        self.assertEqual(len(recurring_asset), 2, msg=None)


if __name__ == "__main__":
    unittest.main()
