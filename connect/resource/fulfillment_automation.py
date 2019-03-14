# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from typing import Any

from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from connect.models.fulfillment import Fulfillment
from connect.models.tier_config import TierConfigFulfillment
from .fulfillment import FulfillmentResource


class FulfillmentAutomation(FulfillmentResource):

    def process(self):
        # type: () -> Any
        for tier_config in self.tier_configs_list:
            self.dispatch_tier_config(tier_config)
        for request in self.list:
            self.dispatch(request)

    def dispatch(self, request):
        # type: (Fulfillment) -> Any
        try:
            logger.info('Start request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            if not result:
                logger.info('Method `process_request` did not return result')
                return

            params = {}
            if isinstance(result, ActivationTileResponse):
                params = {'activation_tile': result.tile}
            elif isinstance(result, ActivationTemplateResponse):
                params = {'template_id': result.template_id}

            self.approve(request.id, params)

        except FulfillmentInquire as inquire:
            self.update_parameters(request.id, inquire.params)
            return self.inquire(request.id)

        except FulfillmentFail as fail:
            return self.fail(request.id, reason=fail.message)

        except Skip as skip:
            return skip.code

        return

    def process_request(self, request):
        # type: (Fulfillment) -> Any
        raise NotImplementedError('Please implement `process_request` logic')

    def dispatch_tier_config(self, tier_config):
        # type: (TierConfigFulfillment) -> Any
        try:
            if self.config.products and tier_config.configuration.product.id not in self.config.products:
                pass
        except FulfillmentInquire as inquire:
            self.update_parameters(tier_config.id, inquire.params)
            return self.inquire(tier_config.id)

        except FulfillmentFail as fail:
            return self.fail(tier_config.id, reason=fail.message)

        except Skip as skip:
            return skip.code

        return
