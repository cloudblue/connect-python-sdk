# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from abc import ABCMeta

from typing import Any, Optional

from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Param
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from connect.models.tier_config import TierConfigRequest, TierConfigRequestSchema, TierConfig
from .automation import AutomationResource


class TierConfigAutomation(AutomationResource):
    __metaclass__ = ABCMeta
    resource = 'tier/config-requests'
    schema = TierConfigRequestSchema()

    def dispatch(self, request):
        # type: (TierConfigRequest) -> Any
        try:
            if self.config.products \
                    and request.configuration.product.id not in self.config.products:
                return 'Invalid product'

            logger.info(
                'Start tier config request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            if not result:
                logger.info('Method `process_request` did not return result')
                return

            params = {}
            if isinstance(result, ActivationTileResponse):
                params = {'template': {'representation': result.tile}}
            elif isinstance(result, ActivationTemplateResponse):
                params = {'template': {'id': result.template_id}}

            self.approve(request.id, params)

        except FulfillmentInquire as inquire:
            self.update_parameters(request.id, inquire.params)
            return self.inquire(request.id)

        except FulfillmentFail as fail:
            return self.fail(request.id, reason=fail.message)

        except Skip as skip:
            return skip.code

        return

    def get_tier_config(self, tier_id, product_id):
        # type: (str, str) -> Optional[TierConfig]
        params = {
            'status': 'approved',
            'configuration__product__id': product_id,
            'configuration__account__id': tier_id,
        }
        response = self.api.get(url=self._list_url, params=params)
        objects = self._load_schema(response)

        if isinstance(objects, list) and len(objects) > 0:
            # Return configuration field if defined, otherwise create TierConfig from request
            return objects[0].configuration \
                if objects[0].configuration.id \
                else TierConfig(**vars(objects[0]))
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
