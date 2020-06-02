# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
import unittest

from mock import Mock, patch

from connect.config import Config
from connect.resources.subscription import Subscription
from connect.models import BillingRequest
from .common import Response, load_json, load_str

add_billing_request_body = load_json(
    os.path.join(os.path.dirname(__file__), 'data', 'add_billing_request.json'))
add_billing_request_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_add_billing_request.json'))


class testSubscriptions(unittest.TestCase):

    def setUp(self):
        self.config = Config(file='tests/config.json')

    @patch('requests.post')
    def test_create_billing_request(self, post_mock):
        # type: (Mock) -> None
        post_mock.return_value = Response(True, add_billing_request_response, 200)
        body = add_billing_request_body
        request = Subscription(config=self.config)
        billing_request = request.create_billing_request(body)
        assert isinstance(billing_request, BillingRequest)
        assert billing_request.id == 'BRP-6750-9514-7931-0001'

    @patch('requests.put')
    def test_update_billing_request(self, put_mock):
        update_billing_request_response = {'provider': {'external_id': '321-123'}}
        put_mock.return_value = Response(True, update_billing_request_response, 200)
        body = update_billing_request_response
        pk = 'BRP-6750-9514-7931-0001'
        request = Subscription(config=self.config)
        billing_request = request.update_billing_request(pk, body)
        assert billing_request == ({'provider': {'external_id': '321-123'}}, 200)


if __name__ == "__main__":
    unittest.main()
