# -*- coding: utf-8 -*-
# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
import pytest
import unittest
from mock import patch
from connect.resources.asset_request import AssetRequestResource
from connect.config import Config
from .common import load_str

update_param_asset_request_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'update_param_asset_request_response.json'))


class TestAssetRequest(unittest.TestCase):
    def setUp(self):
        self.config = Config(file='tests/config.json')

    @patch('requests.put')
    def test_update_param_asset_request(self, put_mock):
        request = AssetRequestResource(config=self.config)
        pr_id = 'PR-4405-9454-9305-001'
        test_data = {
            "params": [{
                "id": "PM-9861-7949-8492-0001",
                "value": "32323323"
            }]
        }
        request.update_param_asset_request(pr_id, test_data, "i'm a note!")
        assert put_mock.call_count == 1
        put_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url=('http://localhost:8080/api/public/v1/'
                 'requests/PR-4405-9454-9305-001/'),
            json={
                'asset': test_data,
                'note': "i'm a note!",
            })

    def test_invalid_request_id(self):
        asset_request = AssetRequestResource(config=self.config)
        with pytest.raises(ValueError) as e:
            asset_request.update_param_asset_request(None, None, None)
        assert str(e.value) == 'Invalid ID'


if __name__ == "__main__":
    unittest.main()
