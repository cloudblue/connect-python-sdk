# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from typing import Any, Optional, Union

from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Param
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from connect.models.tier_config import TierConfigRequest, TierConfigRequestSchema, TierConfig
from .fulfillment import FulfillmentResource


class TierConfigRequestAutomation(FulfillmentResource):
    resource = 'tier/config-requests'
    schema = TierConfigRequestSchema(many=True)

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

    def get_tier_config(self, tier_id, product_id):
        # type: (str, str) -> Optional[Union[TierConfig, TierConfigRequest]]
        params = {
            'status': 'approved',
            'configuration__product__id': product_id,
            'configuration__account__id': tier_id,
        }
        response = self.api.get(url=self._list_url(), params=params)
        objects = self._loads_schema(response)

        if isinstance(objects, list) and len(objects) > 0:
            # Return configuration field if defined, otherwise the TierConfigRequest itself
            return objects[0].configuration \
                if objects[0].configuration.id \
                else objects[0]
        else:
            # Return the object or, if an empty list, None
            return objects or None

    def get_tier_config_param(self, param_id, tier_id, product_id):
        # type: (str, str, str) -> Optional[Param]
        tier_config = self.get_tier_config(tier_id, product_id)
        if not tier_config:
            return None

        params = [param for param in tier_config.params if param.id == param_id]
        return params[0] if len(params) > 0 else None
