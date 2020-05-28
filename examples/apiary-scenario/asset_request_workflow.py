# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.
""" This is part of the example of the implementation between connect and
a Vendor System API.
The detail of this scenario is documented in the documentation portal
https://connect.cloudblue.com/community/sdk/
This microservice search all of the Purchase Request in status pending in Connect
and creates the request in the Vendor System using Vendor System API.
"""

import warnings
import requests

from connect.config import Config
from connect.logger import logger
from connect.models import AssetRequest
from connect.resources.automation_engine import AutomationEngine
from connect.resources.fulfillment import Fulfillment

# URL of the Vendor API, in this case the apiary.io scenario
VENDOR_API_URL = 'https://SET_YOUR_OWN_SAMPLE.apiary-mock.com/'

# Enable processing of deprecation warnings
warnings.simplefilter('default')

# Set logger level / default level ERROR
logger.setLevel('DEBUG')

# If we remove this line, it is done implicitly
Config(file='examples/apiary-scenario/config.json')


class AssetRequest(AutomationEngine):
    resource = 'requests'
    model_class = AssetRequest

    def __init__(self, config=None):
        super().__init__(config=config)
        self._fulfillment = Fulfillment(config)

    def dispatch(self, request):
        return self.process_request(request)

    def process_request(self, request):
        if (request.type == 'purchase'):
            if (len(request.asset.items) == 1):
                tenant_param_id = ''
                for param in request.asset.params:
                    if (param.name == 'tenantId'):
                        tenant_param_id = param.value
                if (tenant_param_id == ''):
                    self.create_request(request)
                else:
                    logger.info('Skip process')
            else:
                logger.info('Request malformed, too many items')
        else:
            logger.info('This processor not handle this type of request')
        return False

    def create_request(self, request):
        for item in request.asset.items:
            mpn = item.mpn
            quantity = item.quantity
            break

        url = VENDOR_API_URL + "tenant?externalId=" + mpn
        response = requests.get(url, data='').json()
        first_name = request.asset.tiers.customer.contact_info.contact.first_name
        last_name = request.asset.tiers.customer.contact_info.contact.last_name
        address = request.asset.tiers.customer.contact_info.address_line1
        postal_code = request.asset.tiers.customer.contact_info.postal_code
        country = request.asset.tiers.customer.contact_info.country
        email = request.asset.tiers.customer.contact_info.contact.email
        account_phone = request.asset.tiers.customer.contact_info.contact.phone_number.phone_number
        if response['externalId'] != request.asset.id:
            url = VENDOR_API_URL + 'tenant'
            payload = {
                'Attributes': {
                    'product': {
                        'item': mpn,
                        'quantity': quantity
                        },
                    'account': {
                        'accountFirstName': first_name,
                        'accountLastName': last_name,
                        'accountCompany': request.asset.tiers.customer.name,
                        'accountAddress': address,
                        'accountCity': request.asset.tiers.customer.contact_info.city,
                        'accountState': request.asset.tiers.customer.contact_info.state,
                        'accountPostalCode': postal_code,
                        'accountCountry': country,
                        'accountEmail': email,
                        'accountPhone': account_phone
                        }
                    }
                }
            response = requests.post(url, data=payload).json()
            if (response['tenantId'] != ''):
                data = {
                    "params": [{
                        "id": "tenantId",
                        "value": response['tenantId']
                    }]
                }
                self._fulfillment.update_param_asset_request(request.id, data, 'vendor system Id')
                return response
            else:
                logger.info('Error in Vendor System')
                return False


if __name__ == '__main__':
    asset_request_example = AssetRequest()
    asset_request_example.process()
