# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from abc import ABCMeta

from typing import Any, Dict

from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from connect.models.fulfillment import Fulfillment, FulfillmentSchema
from .automation import AutomationResource


class FulfillmentAutomation(AutomationResource):
    __metaclass__ = ABCMeta
    resource = 'requests'
    schema = FulfillmentSchema(many=True)

    def build_filter(self, status='pending'):
        # type: (str) -> Dict[str, Any]
        filters = super(FulfillmentAutomation, self).build_filter(status)
        if self.config.products:
            filters['asset.product.id__in'] = ','.join(self.config.products)
        return filters

    def dispatch(self, request):
        # type: (Fulfillment) -> str
        try:
            if self.config.products \
                    and request.asset.product.id not in self.config.products:
                return 'Invalid product'

            logger.info('Start request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            if not result:
                logger.info('Method `process_request` did not return result')
                return ''

            params = {}
            if isinstance(result, ActivationTileResponse):
                params = {'activation_tile': result.tile}
            elif isinstance(result, ActivationTemplateResponse):
                params = {'template_id': result.template_id}

            return self.approve(request.id, params)

        except FulfillmentInquire as inquire:
            self.update_parameters(request.id, inquire.params)
            return self.inquire(request.id)

        except FulfillmentFail as fail:
            return self.fail(request.id, reason=fail.message)

        except Skip as skip:
            return skip.code
