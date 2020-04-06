# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import Union
import warnings

from connect.config import Config
from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Fulfillment
from connect.resources import FulfillmentAutomation

# Enable processing of deprecation warnings
warnings.simplefilter('default')

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
                        raise FailRequest('Is not possible to purchase product in such quantities')

                for param in request.asset.params:
                    if param.name == 'email' and not param.value:
                        param.value_error = 'Email address has not been provided, ' \
                                            'please provide one'
                        raise InquireRequest(params=[param])

                # Find a param by its id
                param = request.asset.get_param_by_id('purchase_id')
                if param:
                    param.value = '...'  # We can assign the id given by the external service here
                    self.update_parameters(request.id, [param])  # Update param on the platform
                else:
                    raise FailRequest('The asset is expected to have a "purchase_id" param.')

                # Approve by Template
                return ActivationTemplateResponse('TL-497-535-242')
                # Or
                # return TemplateResource().get(pk='TEMPLATE_ID')

                # Approve by ActivationTile
                # return ActivationTileResponse('\n  # Welcome to Fallball!\n\nYes, you decided '
                #                              'to have an account in our amazing service!')
                # Or
                # return TemplateResource().render(pk='TEMPLATE_ID', request_id=request.id)

            elif request.type == 'change':
                # Fail
                raise FailRequest()
            else:
                # Skip request
                raise SkipRequest()


if __name__ == '__main__':
    fulfillment_example = FulfillmentExample()
    fulfillment_example.process()
