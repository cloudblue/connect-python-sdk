# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.
import json
from connect.config import Config
from connect.resources.subscription import Subscription


class RecurringAsset():
    configuration = Config(file='examples/config.json')

    def list_recurring_asset(self):
        tier = Subscription(config=self.configuration)
        return tier._recurring_asset.list()

    def get_recurring_asset(self, id):
        tier = Subscription(config=self.configuration)
        return tier._recurring_asset.get(id)


def main():
    recurring_asset_example = RecurringAsset()
    with open('./tests/data/tier_configuration_request.json') as json_file:
        data = json.load(json_file)
    recurring_asset_example.create_tier_account_request(data)
    result = recurring_asset_example.get_recurring_asset('AS-3110-7077-0368')
    print(result.status)


if __name__ == '__main__':
    main()
