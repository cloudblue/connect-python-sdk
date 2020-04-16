# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.
import json
from connect.config import Config
from connect.resources.subscription import Subscription


class BillingRequest():
    configuration = Config(file='examples/config.json')

    def list_billing_request(self):
        tier = Subscription(config=self.configuration)
        return tier._billing_request.list()

    def get_billing_request(self, id):
        tier = Subscription(config=self.configuration)
        return tier._billing_request.get(id)


def main():
    billing_request_example = BillingRequest()
    with open('./tests/data/tier_configuration_request.json') as json_file:
        data = json.load(json_file)
    billing_request_example.create_tier_account_request(data)

    ''' List example '''
    billing_request = billing_request_example.list_billing_request()
    print(billing_request[0].id)


if __name__ == '__main__':
    main()
