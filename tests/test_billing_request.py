# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
import unittest
import pytest

from mock import Mock, call, patch

from connect.config import Config
from connect.models import BillingRequest
from connect.resources.billing_request import BillingRequestResource

from .common import Response, load_json, load_str

get_billing_request_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_get_billing_request.json'))
list_billing_request_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_list_billing_request.json'))
add_billing_request_body = load_json(
    os.path.join(os.path.dirname(__file__), 'data', 'add_billing_request.json'))
add_billing_request_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_add_billing_request.json'))


class testBillingRequest(unittest.TestCase):

    def setUp(self):
        self.config = Config(file='tests/config.json')

    @patch('requests.get')
    def test_get_billing_request_ok(self, get_mock):
        # type: (Mock) -> None
        get_mock.side_effect = [
            Response(True, '[' + get_billing_request_contents + ']', 200),
            Response(True, get_billing_request_contents, 200)
        ]

        request = BillingRequestResource(config=self.config)
        billing_request = request.get('BRP-3110-7077-0368-0001')
        assert get_mock.call_count == 1
        self.assertEqual(billing_request.type, 'provider', msg=None)
        # 054922da-ceae-47de-8e5d-7a2950acbfe1

        get_mock.assert_has_calls([
            call(
                headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
                timeout=300,
                url=('http://localhost:8080/api/public/v1/'
                     'subscriptions/requests/BRP-3110-7077-0368-0001'))
        ])
        assert isinstance(billing_request, BillingRequest)

    @patch('requests.get')
    def test_billing_request_empty(self, get_mock):
        # type: (Mock) -> None
        get_mock.return_value = Response(True, '[]', 200)

        request = BillingRequestResource(config=self.config)
        billing_request = request.get('BPR-0000-0000-0000-0000')
        assert get_mock.call_count == 1
        url = 'http://localhost:8080/api/public/v1/subscriptions/requests/BPR-0000-0000-0000-0000'
        get_mock.assert_has_calls([
            call(
                headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
                timeout=300,
                url=url
                )
        ])
        self.assertEqual(billing_request, [], msg=None)

    @patch('requests.get')
    def test_list_billing_request_ok(self, get_mock):
        # type: (Mock) -> None
        get_mock.side_effect = [
            Response(True, list_billing_request_contents, 200)
        ]

        request = BillingRequestResource(config=self.config)
        billing_request = request.list()
        assert get_mock.call_count == 1

        get_mock.assert_has_calls([
            call(
                headers={'Authorization': 'ApiKey XXXX:YYYYY', 'Content-Type': 'application/json'},
                timeout=300,
                url='http://localhost:8080/api/public/v1/subscriptions/requests?limit=100')
        ])
        self.assertEqual(len(billing_request), 2, msg=None)

    @patch('requests.post')
    def test_add_billing_request(self, post_mock):
        # type: (Mock) -> None
        post_mock.return_value = Response(True, add_billing_request_response, 200)
        body = add_billing_request_body
        request = BillingRequestResource(config=self.config)
        billing_request = request.create(body)

        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json=body,
            timeout=300,
            url='http://localhost:8080/api/public/v1/subscriptions/requests')
        assert isinstance(billing_request, BillingRequest)
        assert billing_request.id == 'BRP-6750-9514-7931-0001'

    @patch('requests.put')
    def test_modify_billing_request(self, put_mock):
        modify_billing_request_response = {'provider': {'external_id': '321-123'}}
        put_mock.return_value = Response(True, modify_billing_request_response, 200)
        body = modify_billing_request_response
        pk = 'BRP-6750-9514-7931-0001'
        request = BillingRequestResource(config=self.config)
        billing_request = request.update_billing_request(pk, body)
        url = ('http://localhost:8080/api/public/v1'
               '/subscriptions/requests/BRP-6750-9514-7931-0001/attributes')
        put_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json=body,
            timeout=300,
            url=url)
        assert billing_request == ({'provider': {'external_id': '321-123'}}, 200)

    def test_update_billing_request_bad(self):
        request = BillingRequestResource(config=self.config)
        with pytest.raises(ValueError) as e:
            request.update_billing_request(None, None)
        assert str(e.value) == 'Invalid ID'


if __name__ == "__main__":
    unittest.main()
