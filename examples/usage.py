# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from datetime import date, timedelta
import time

from connect.models import Contract, UsageRecord, UsageFile, UsageListing, Product
from connect.resources import UsageAutomation


class UsageExample(UsageAutomation):
    def process_request(self, request):
        # type: (UsageListing) -> None

        # Detect specific provider contract
        if request.contract.id == 'CRD-41560-05399-123':
            # Can also be seen from request.provider.id and parametrized further
            # via marketplace available at request.marketplace.id
            usage_file = UsageFile(
                name='sdk test',
                product=Product(id=request.product.id),
                contract=Contract(id=request.contract.id)
            )

            usages = [
                UsageRecord(
                    record_id='unique record value',

                    item_search_criteria='item.mpn',
                    # Possible values are item.mpn or item.local_id.

                    item_search_value='SKUA',
                    # Value defined as MPN on vendor portal.

                    quantity=1,
                    # Quantity to be reported.

                    start_time_utc=(date.today() - timedelta(1)).strftime('%Y-%m-%d'),
                    # From when to report.

                    end_time_utc=time.strftime('%Y-%m-%d %H:%M:%S'),
                    # Till when to report.

                    asset_search_criteria='parameter.param_b',
                    # How to find the asset on Connect.  Typical use case is to use a parameter
                    # provided by vendor, in this case called param_b.  Additionally, asset.id
                    # can be used in case you want to use Connect identifiers.

                    asset_search_value='tenant2'
                )
            ]

            self.submit_usage(usage_file, usages)
        else:
            # Something different could be done here
            pass


if __name__ == '__main__':
    usage_example = UsageExample()
    usage_example.process()
