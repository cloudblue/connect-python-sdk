# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.
import json
from connect.config import Config
from connect.resources.fulfillment import FulfillmentResource


class AssetRequest():
    configuration = Config(file='examples/config.json')

    def list_asset_request(self):
        asset_request = FulfillmentResource(config=self.configuration)
        return asset_request.search_asset_request()

    def create_asset_request(self, body):
        asset_request = FulfillmentResource(config=self.configuration)
        return asset_request.create_purchase_request(body)


def main():
    asset_request_example = AssetRequest()
    with open('./tests/data/create_purchase_request_body_param.json') as json_file:
        body = json.load(json_file)
    result = asset_request_example.create_asset_request(body)
    for asset in result:
        print(asset.id)


if __name__ == '__main__':
    main()
