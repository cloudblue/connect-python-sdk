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
Config(file='config.json')


class AssetRequest(AutomationEngine):

    model_class = Fulfillment
    resource = 'requests'

    logger = logging.getLogger('Fullfilment.logger')

    def dispatch(self, request):
        return self.process_request(request)

    def process_request(self, request):
        for item in request.asset.items:
            npm = item.mpn
            quantity = item.quantity
            break

        url = VENDOR_API_URL + "tenant?externalId=" + npm
        response = requests.get(url, data='').json()
        firstName = request.asset.tiers.customer.contact_info.contact.first_name
        lastName = request.asset.tiers.customer.contact_info.contact.last_name
        address = request.asset.tiers.customer.contact_info.address_line1
        postalCode = request.asset.tiers.customer.contact_info.postal_code
        accountPhone = request.asset.tiers.customer.contact_info.contact.phone_number.phone_number
        if response['externalId'] != request.asset.id:
            url = VENDOR_API_URL + "tenant"
            payload = {
                    'Attributes': {
                        'product': {
                            'item': npm,
                            'quantity': quantity
                        },
                        'account': {
                            'accountFirstName': firstName,
                            'accountLastName': lastName,
                            'accountCompany': request.asset.tiers.customer.name,
                            'accountAddress': address,
                            'accountCity': request.asset.tiers.customer.contact_info.city,
                            'accountState': request.asset.tiers.customer.contact_info.state,
                            'accountPostalCode': postalCode,
                            'accountCountry': request.asset.tiers.customer.contact_info.country,
                            'accountEmail': request.asset.tiers.customer.contact_info.contact.email,
                            'accountPhone': accountPhone
                        }
                    }
                }
            response = requests.post(url, data=payload).json()
        return response


if __name__ == '__main__':
    asset_request_example = AssetRequest()
    asset_request_example.process()
