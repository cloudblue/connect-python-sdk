# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from connect import FulfillmentAutomation
from connect.config import Config
from connect.logger import logger
# noinspection PyUnresolvedReferences
from connect.models import ActivationTemplateResponse, ActivationTileResponse
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip

# Set logger level / default level ERROR
logger.setLevel("DEBUG")


class ExampleRequestProcessor(FulfillmentAutomation):
    def process_request(self, req):

        # Custom logic
        if req.type == 'purchase':
            for item in req.asset.items:
                if item.quantity > 100000:
                    raise FulfillmentFail(
                        message='Is Not possible to purchase product')

            for param in req.asset.params:
                if param.name == 'email' and not param.value:
                    param.value_error = 'Email address has not been provided, please provide one'
                    raise FulfillmentInquire(params=[param])

            # Approve by ActivationTile
            return ActivationTileResponse('\n  # Welcome to Fallball!\n\nYes, you decided '
                                          'to have an account in our amazing service!')
            # Or
            # return TemplateResource(self.config).render(pk='TEMPLATE_ID', request_id=req.id)

            # Approve by Template
            # return ActivationTemplateResponse('TL-497-535-242')
            # Or
            # return TemplateResource(self.config).get(pk='TEMPLATE_ID')

        elif req.type == 'change':
            # fail
            raise FulfillmentFail()
        else:
            # skip request
            raise Skip()


if __name__ == '__main__':
    request = ExampleRequestProcessor(Config(filename='config.json'))
    request.process()
