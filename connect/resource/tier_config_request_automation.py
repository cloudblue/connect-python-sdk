# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from typing import Any

from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from connect.models.tier_config import TierConfigRequest
from .fulfillment import FulfillmentResource


class TierConfigRequestAutomation(FulfillmentResource):
    resource = 'tier/config-requests'

    def build_filter(self):
        # type: () -> dict

        # Skip parent class and go directly to BaseResource.build_filter()
        filters = super(FulfillmentResource, self).build_filter()

        filters['status'] = 'pending'
        return filters

    def process(self):
        # type: () -> Any
        for request in self.list:
            self.dispatch(request)

    def dispatch(self, tier_config):
        # type: (TierConfigRequest) -> Any
        try:
            if self.config.products \
                    and tier_config.configuration.product.id not in self.config.products:
                return 'Invalid product'

            logger.info(
                'Start tier config request process / ID request - {}'.format(tier_config.id))
            result = self.process_request(tier_config)

            if not result:
                logger.info('Method `process_tier_config_request` did not return result')
                return

            params = {}
            if isinstance(result, ActivationTileResponse):
                params = {'template': {'representation': result.tile}}
            elif isinstance(result, ActivationTemplateResponse):
                params = {'template': {'id': result.template_id}}

            self.approve(tier_config.id, params)

        except FulfillmentInquire as inquire:
            self.update_parameters(tier_config.id, inquire.params)
            return self.inquire(tier_config.id)

        except FulfillmentFail as fail:
            return self.fail(tier_config.id, reason=fail.message)

        except Skip as skip:
            return skip.code

        return

    def process_request(self, tier_config_request):
        # type: (TierConfigRequest) -> Any
        raise NotImplementedError('Please implement `process` logic')
