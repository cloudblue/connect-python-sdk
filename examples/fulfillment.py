# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import Union

from connect.config import Config
from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Fulfillment
from connect.resources import FulfillmentAutomation

# Set logger level / default level ERROR
logger.setLevel('DEBUG')

# If we remove this line, it is done implicitly
Config(file='config.json')


class FulfillmentExample(FulfillmentAutomation):
    def process_request(self, request):
        # type: (Fulfillment) -> Union[ActivationTemplateResponse, ActivationTileResponse]

        if request.needs_migration():
            # Skip request if it needs migration (migration is performed by an external service)
            logger.info('Skipping request {} because it needs migration.'.format(request.id))
            raise SkipRequest()
        else:
            logger.info('Processing request {} for contract {}, product {}, marketplace {}'
                        .format(request.id,
                                request.contract.id,
                                request.asset.product.name,
                                request.marketplace.name))

            # Custom logic
            if request.type == 'purchase':
                for item in request.asset.items:
                    if item.quantity > 100000:
                        raise FailRequest(
                            message='Is Not possible to purchase product')

                for param in request.asset.params:
                    if param.name == 'email' and not param.value:
                        param.value_error = 'Email address has not been provided, ' \
                                            'please provide one'
                        raise InquireRequest(params=[param])

                # Approve by ActivationTile
                return ActivationTileResponse('\n  # Welcome to Fallball!\n\nYes, you decided '
                                              'to have an account in our amazing service!')
                # Or
                # return TemplateResource().render(pk='TEMPLATE_ID', request_id=request.id)

                # Approve by Template
                # return ActivationTemplateResponse('TL-497-535-242')
                # Or
                # return TemplateResource().get(pk='TEMPLATE_ID')

            elif request.type == 'change':
                # Fail
                raise FailRequest()
            else:
                # Skip request
                raise SkipRequest()


if __name__ == '__main__':
    fulfillment_example = FulfillmentExample()
    fulfillment_example.process()
