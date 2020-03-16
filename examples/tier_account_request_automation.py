# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.
# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.
import json
from connect.config import Config
from connect.resources.fulfillment import Fulfillment
from connect.resources.directory import Directory
from connect.resources import TierAccountRequestAutomation

class TierAccountRequestExample(TierAccountRequestAutomation):
    configuration = Config(file='examples/config.json')

    def process_request(self, request):
        pass
        # return TierAccountRequestAutomation.dispatch(self, request)

def main():
    tier_account_example = TierAccountRequestExample()
    with open('./tests/data/tier_configuration_request.json') as json_file:
        data = json.load(json_file)
    # tier_account_example.create_tier_account_request(data)
    print(tier_account_example.process())

if __name__ == '__main__':
    main()