# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.
from connect.resources.tier_account_request_automation import (
    TierAccountRequestAutomation,
    TierAccountRequestAction,
)
from connect.config import Config


class MyExampleTARAutomation(TierAccountRequestAutomation):
    def process_request(self, request):
        if request.account.contact_info.country == 'AR':
            stat = TierAccountRequestAction(TierAccountRequestAction.ACCEPT)
            print(stat)
            return stat
        elif request.account.contact_info.country == 'IT':
            stat = TierAccountRequestAction(TierAccountRequestAction.IGNORE, 'No data')
            print(stat)
            return stat
        else:
            stat = TierAccountRequestAction(TierAccountRequestAction.SKIP)
            # print(stat)
            return stat


if __name__ == '__main__':
    configuration = Config(file='examples/config.json')
    tier_account_example = MyExampleTARAutomation(config=configuration)
    tier_account_example.process()
