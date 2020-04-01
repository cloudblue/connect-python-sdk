# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

import os
import unittest
from connect.models import TierConfigRequest
from connect.resources.fulfillment import TierConfigRequestResource
from connect.config import Config
from .common import Response, load_str
from mock import patch, call

get_tier_config_request_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'get_tier_config_request_response.json'))
list_tier_config_request_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'list_tier_config_request_response.json'))
create_tier_config_request_body = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'create_tier_config_request_body.json'))

class TestTierConfigRequest(unittest.TestCase):
    def setUp(self):
        self.config = Config(file='tests/config.json')
   
    @patch('requests.get')
    def test_get_tier_config_request_ok(self, get_mock):
        # type: (Mock) -> None
        get_mock.side_effect = [
            Response(True, '[' + get_tier_config_request_contents + ']', 200),
            Response(True, get_tier_config_request_contents, 200)
        ]
        request = TierConfigRequestResource(config=self.config)
        tier_config_request = request.get('TCR-6458-9737-0065-004-001')
        assert get_mock.call_count == 1
        self.assertEqual(tier_config_request.status, 'pending', msg=None)
        # 054922da-ceae-47de-8e5d-7a2950acbfe1
        get_mock.assert_has_calls([
            call(
                headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
                timeout=300,
                url='http://localhost:8080/api/public/v1/tier/config-requests/TCR-6458-9737-0065-004-001')
        ])
        assert isinstance(tier_config_request, TierConfigRequest)
    
    @patch('requests.get')
    def test_list_tier_config_request_ok(self, get_mock):
        # type: (Mock) -> None
        get_mock.side_effect = [
            Response(True, list_tier_config_request_contents, 200)
        ]
        request = TierConfigRequestResource(config=self.config)
        tier_config_request = request.list()
        assert get_mock.call_count == 1
        get_mock.assert_has_calls([
            call(
                headers={'Authorization': 'ApiKey XXXX:YYYYY', 'Content-Type': 'application/json'},
                params={'limit': 100},
                timeout=300,
                url='http://localhost:8080/api/public/v1/tier/config-requests')
        ])
        self.assertEqual(len(tier_config_request), 3, msg=None)
    '''
    @patch('requests.post')
    def test_create_tier_config_request(self, post_mock):
        # type: (Mock) -> None
        body_return = {
            "error_code": "VAL_001",
            "errors": ["errors: ['Tier Configuration with this Tier level, Tier and Product already exists.']"]
        }
        post_mock.return_value = Response(True, body_return, 200)
        # print(body)
        request = TierConfigRequestResource(config=self.config)
        tier_config_request = request.create(create_tier_config_request_body)
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json=create_tier_config_request_body,
            timeout=300,
            url='http://localhost:8080/api/public/v1/tier/config-requests')
        assert tier_config_request[0].id == 'TAR-6458-9737-0065-004-001'

    '''
    @patch('requests.post')
    def test_inquire_tier_account_request(self, post_mock):
        # type: (Mock) -> None
        post_mock.return_value = Response(True, '', 204)
        request = TierConfigRequestResource(config=self.config)
        id_tar = 'TAR-6458-9737-0065-004-001'
        tier_config_request = request.inquire(id_tar)
        assert post_mock.call_count == 1
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url='http://localhost:8080/api/public/v1/tier/config-requests/TAR-6458-9737-0065-004-001/inquire')
        assert tier_config_request == ('', 204)

    @patch('requests.post')
    def test_pending_tier_account_request(self, post_mock):
        # type: (Mock) -> None
        post_mock.return_value = Response(True, '', 200)
        request = TierConfigRequestResource(config=self.config)
        id_tar = 'TAR-6458-9737-0065-004-001'
        tier_config_request = request.pend(id_tar)
        assert post_mock.call_count == 1
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url='http://localhost:8080/api/public/v1/tier/config-requests/TAR-6458-9737-0065-004-001/pend')
        assert tier_config_request == ('', 200)

    @patch('requests.post')
    def test_assign_tier_account_request(self, post_mock):
        # type: (Mock) -> None
        post_mock.return_value = Response(True, '', 200)
        request = TierConfigRequestResource(config=self.config)
        id_tar = 'TAR-6458-9737-0065-004-001'
        tier_config_request = request.assign(id_tar)
        assert post_mock.call_count == 1
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url='http://localhost:8080/api/public/v1/tier/config-requests/TAR-6458-9737-0065-004-001/assign')
        assert tier_config_request == ('', 200)

    @patch('requests.post')
    def test_unassign_tier_account_request(self, post_mock):
        # type: (Mock) -> None
        post_mock.return_value = Response(True, '', 200)
        request = TierConfigRequestResource(config=self.config)
        id_tar = 'TAR-6458-9737-0065-004-001'
        tier_config_request = request.unassign(id_tar)
        assert post_mock.call_count == 1
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url='http://localhost:8080/api/public/v1/tier/config-requests/TAR-6458-9737-0065-004-001/unassign')
        assert tier_config_request == ('', 200)

    @patch('requests.post')
    def test_approve_tier_account_request(self, post_mock):
        # type: (Mock) -> None
        body_request = {"template": {"id": "TP-1234-123-123"}}
        body_response = {"template": {"id": "TP-123-123-123", "representation": "Rendered template" }}
        post_mock.return_value = Response(True, body_response, 200)
        request = TierConfigRequestResource(config=self.config)
        id_tar = 'TAR-6458-9737-0065-004-001'
        tier_config_request = request.approve(id_tar, 'TP-1234-123-123')
        assert post_mock.call_count == 1
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            json=body_request, 
            url='http://localhost:8080/api/public/v1/tier/config-requests/TAR-6458-9737-0065-004-001/approve')
        assert tier_config_request == (body_response, 200)

    @patch('requests.post')
    def test_fail_tier_account_request(self, post_mock):
        # type: (Mock) -> None
        body_request = {"reason": "some reason"}
        post_mock.return_value = Response(True, '', 204)
        request = TierConfigRequestResource(config=self.config)
        id_tar = 'TAR-6458-9737-0065-004-001'
        tier_config_request = request.fail(id_tar, 'some reason')
        assert post_mock.call_count == 1
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            json=body_request, 
            url='http://localhost:8080/api/public/v1/tier/config-requests/TAR-6458-9737-0065-004-001/fail')
        assert tier_config_request == ('', 204)

if __name__ == "__main__":
    unittest.main()
