# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.
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
        print(t_account.id)
        print(t_account.external_id)
        print(t_account.external_uid)
        print(t_account.contact_info.address_line1)

    def accept_tier_account_request(self, id_tar):
        tier = Fulfillment(config=self.configuration)
        response = tier.accept_tier_account_request(id_tar)
        print(response)

    def ignore_tier_account_request(self, id_tar, reason):
        tier = Fulfillment(config=self.configuration)
        response = tier.ignore_tier_account_request(id_tar, reason)
        print(response)

    def create_tier_account_request(self, data):
        tier = Fulfillment(config=self.configuration)
        response = tier.create_tier_account_request(data)
        print(response)

def main():
    tier_account_example = TierAccountRequest()
    with open('./tests/data/tier_configuration_request.json') as json_file:
        data = json.load(json_file)
    # tier_account_example.create_tier_account_request(data)
    print(tier_account_example.get_tier_account())
if __name__ == '__main__':
    main()
