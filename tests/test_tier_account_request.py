# -*- coding: utf-8 -*-
# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
import unittest
from mock import patch, call
from connect.models import TierAccountRequest
from connect.resources.tier_account import TierAccountRequestResource
from connect.config import Config
from .common import Response, load_str

get_tier_account_request_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_get_tier_account_request.json'))
list_tier_account_request_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_list_tier_account_request.json'))
create_tier_account_request_body = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'create_tier_account_request_body.json'))
create_tier_account_request_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'create_tier_account_request_response.json'))
accept_tier_account_request_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'accept_tier_account_request_response.json'))
ignore_tier_account_request_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'ignore_tier_account_request_response.json'))


class TestTierAccountRequest(unittest.TestCase):
    def setUp(self):
        self.config = Config(file='tests/config.json')

    @patch('requests.get')
    def test_get_tier_account_request_ok(self, get_mock):
        get_mock.side_effect = [
            Response(True, '[' + get_tier_account_request_contents + ']', 200),
            Response(True, get_tier_account_request_contents, 200)
        ]

        request = TierAccountRequestResource(config=self.config)
        tier_account_request = request.get('TAR-6458-9737-0065-004-001')
        assert get_mock.call_count == 1
        self.assertEqual(tier_account_request.status, 'pending', msg=None)
        # 054922da-ceae-47de-8e5d-7a2950acbfe1
        get_mock.assert_has_calls([
            call(
                headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
                timeout=300,
                url=('http://localhost:8080/api/public/'
                     'v1/tier/account-requests/TAR-6458-9737-0065-004-001'))
        ])
        assert isinstance(tier_account_request, TierAccountRequest)

    @patch('requests.get')
    def test_get_tier_account_request_empty(self, get_mock):
        get_mock.return_value = Response(True, '[]', 200)

        request = TierAccountRequestResource(config=self.config)
        tier_account_request = request.get('TAR-0000-0000-0000-000-000')
        assert get_mock.call_count == 1

        get_mock.assert_has_calls([
            call(
                headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
                timeout=300,
                url=('http://localhost:8080/api/public/v1/'
                     'tier/account-requests/TAR-0000-0000-0000-000-000'))
        ])
        self.assertEqual(tier_account_request, [], msg=None)

    @patch('requests.get')
    def test_list_tier_account_request_ok(self, get_mock):
        get_mock.side_effect = [
            Response(True, list_tier_account_request_contents, 200)
        ]
        request = TierAccountRequestResource(config=self.config)
        tier_account_request = request.list()
        assert get_mock.call_count == 1
        get_mock.assert_has_calls([
            call(
                headers={'Authorization': 'ApiKey XXXX:YYYYY', 'Content-Type': 'application/json'},
                timeout=300,
                url='http://localhost:8080/api/public/v1/tier/account-requests?limit=100')
        ])
        self.assertEqual(len(tier_account_request), 3, msg=None)

    @patch('requests.post')
    def test_create_tier_account_request(self, post_mock):
        post_mock.return_value = Response(True, create_tier_account_request_response, 200)
        body = create_tier_account_request_body
        request = TierAccountRequestResource(config=self.config)
        tier_account_request = request.create(body)
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json=body,
            timeout=300,
            url='http://localhost:8080/api/public/v1/tier/account-requests')
        assert tier_account_request[0].id == 'TAR-6458-9737-0065-004-001'

    @patch('requests.post')
    def test_accept_tier_account_request(self, post_mock):
        post_mock.return_value = Response(True, accept_tier_account_request_response, 200)
        request = TierAccountRequestResource(config=self.config)
        id_tar = 'TAR-6458-9737-0065-004-001'
        tier_account_request = request.accept(id_tar)
        assert post_mock.call_count == 1
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url=('http://localhost:8080/api/public/v1/'
                 'tier/account-requests/TAR-6458-9737-0065-004-001/accept'))
        assert tier_account_request.id == 'TAR-6458-9737-0065-004-001'

    @patch('requests.post')
    def test_ignore_tier_account_request(self, post_mock):
        post_mock.return_value = Response(True, ignore_tier_account_request_response, 200)
        request = TierAccountRequestResource(config=self.config)
        id_tar = 'TAR-6458-9737-0065-005-001'
        tier_account_request = request.ignore(id_tar, 'some reason')
        assert post_mock.call_count == 1
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            json={'reason': 'some reason'},
            url=('http://localhost:8080/api/public/v1/'
                 'tier/account-requests/TAR-6458-9737-0065-005-001/ignore'))
        assert tier_account_request.id == 'TAR-6458-9737-0065-005-001'


if __name__ == "__main__":
    unittest.main()
