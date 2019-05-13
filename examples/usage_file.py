# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.
from connect.exceptions import AcceptUsageFile, DeleteUsageFile, SkipRequest, SubmitUsageFile
from connect.models import UsageFile
from connect.resources import UsageFileAutomation


class UsageFileExample(UsageFileAutomation):
    def process_request(self, request):
        # type: (UsageFile) -> None
        if request.status == 'invalid':
            # Vendor and provider may handle invalid cases differently,
            # probably notifying their staff
            raise DeleteUsageFile('Not needed anymore')
        elif request.status == 'ready':
            # Vendor may submit file to provider
            raise SubmitUsageFile('Ready for provider')
        elif request.status == 'pending':
            # Provider use case, needs to be reviewed and accepted
            raise AcceptUsageFile('File looks good')
        else:
            raise SkipRequest('Non controlled status')


if __name__ == '__main__':
    usage_file_example = UsageFileExample()
    usage_file_example.process()
