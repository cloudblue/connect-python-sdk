# -*- coding: utf-8 -*-
# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
import unittest
from mock import patch
from connect.resources.asset_request import AssetRequestResource
from connect.config import Config
from .common import Response, load_str

update_param_asset_request_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'update_param_asset_request_response.json'))


class TestAssetRequest(unittest.TestCase):
    def setUp(self):
        self.config = Config(file='tests/config.json')

    @patch('requests.post')
    def update_param_asset_request(self, post_mock):
        post_mock.return_value = Response(True, update_param_asset_request_response, 200)
        request = AssetRequestResource(config=self.config)
        pr_id = 'PR-4405-9454-9305-001'
        asset_request = request(pr_id)
        assert post_mock.call_count == 1
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url=('http://localhost:8080/api/public/v1/'
                 'tier/requests/PR-4405-9454-9305-001'))
        assert asset_request.id == 'PR-4405-9454-9305-001'


if __name__ == "__main__":
    unittest.main()
