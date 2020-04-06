# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.
import json
from connect.config import Config
from connect.resources.fulfillment import Fulfillment
from connect.resources.directory import Directory


class TierAccountRequest():
    configuration = Config(file='examples/config.json')

    def get_pending(self):
        tier = Fulfillment(config=self.configuration)
        return tier.get_pending_tier_account_requests()

    def get_tier_account(self):
        tier = Directory(config=self.configuration)
        t_account = tier.get_tier_account('TA-6458-9737-0065')
        return t_account.id

    def accept_tier_account_request(self, id_tar):
        tier = Fulfillment(config=self.configuration)
        response = tier.accept_tier_account_request(id_tar)
        return response

    def ignore_tier_account_request(self, id_tar, reason):
        tier = Fulfillment(config=self.configuration)
        response = tier.ignore_tier_account_request(id_tar, reason)
        return response

    def create_tier_account_request(self, data):
        tier = Fulfillment(config=self.configuration)
        response = tier.create_tier_account_request(data)
        return response


def main():
    tier_account_example = TierAccountRequest()
    with open('./tests/data/tier_configuration_request.json') as json_file:
        data = json.load(json_file)
    tier_account_example.create_tier_account_request(data)
    print(tier_account_example.get_tier_account())


if __name__ == '__main__':
    main()
