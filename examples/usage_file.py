# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import warnings

from connect.config import Config
from connect.logger import logger
from connect.exceptions import AcceptUsageFile, DeleteUsageFile, SkipRequest, SubmitUsageFile
from connect.models import UsageFile
from connect.resources import UsageFileAutomation

# Enable processing of deprecation warnings
warnings.simplefilter('default')

# Set logger level / default level ERROR
logger.setLevel('DEBUG')

# If we remove this line, it is done implicitly
Config(file='config.json')


class UsageFileExample(UsageFileAutomation):
    def process_request(self, request):
        # type: (UsageFile) -> None
        if request.status == 'invalid':
            # Vendor and provider may handle invalid cases differently,
            # probably notifying their staff
            raise DeleteUsageFile('Not needed anymore')
        elif request.status == 'ready':
            # Vendor may submit file to provider
            raise SubmitUsageFile()
        elif request.status == 'pending':
            # Provider use case, needs to be reviewed and accepted
            raise AcceptUsageFile('File looks good')
        else:
            raise SkipRequest('Non controlled status')


if __name__ == '__main__':
    usage_file_example = UsageFileExample()
    usage_file_example.process()
