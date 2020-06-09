# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.
""" This is part of the example of the implementation between connect and
a Vendor System API.
The detail of this scenario is documented in the documentation portal
https://connect.cloudblue.com/community/sdk/
This microservice search all of the Purchase Request in status pending in Connect
and check the status in the Vendor System. If this status is ready
accept the Purchase Request in connect.
"""

import warnings
import logging
import requests

from connect.config import Config
from connect.logger import logger
from connect.models import Fulfillment
from connect.resources.automation_engine import AutomationEngine

# URL of the Vendor API, in this case the apiary.io scenario
VENDOR_API_URL = 'https://SET_YOUR_OWN_SAMPLE.apiary-mock.com/'

# Enable processing of deprecation warnings
warnings.simplefilter('default')

# Set logger level / default level ERROR
logger.setLevel('DEBUG')

# If we remove this line, it is done implicitly
Config(file='examples/apiary-scenario/config.json')


class AssetAccept(AutomationEngine):

    model_class = Fulfillment
    resource = 'requests'

    logger = logging.getLogger('Fullfilment.logger')

    def dispatch(self, request):
        return self.process_request(request)

    def approve_request(self, request):
        for param in request.asset.configuration.params:
            if (param.id == 'templateId'):
                template_id = param.value
        body = {"activation_tile": template_id}
        response = self.approve(request.id, body)
        return response

    def process_request(self, request):
        if (request.type == 'purchase'):
            for param in request.asset.params:
                if (param.name == 'tenantId'):
                    tenant_param_id = param.value
            url = VENDOR_API_URL + 'tenant/' + request.id
            response = requests.get(url, data='').json()
            if (tenant_param_id != '' and response['status'] == 'ready'):
                self.approve_request(request)
            else:
                logger.info('Skip process')
        else:
            logger.info('This processor not handle this type of request')
        return False


if __name__ == '__main__':
    asset_accept_example = AssetAccept()
    asset_accept_example.process()
