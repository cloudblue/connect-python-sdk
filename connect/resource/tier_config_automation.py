# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from abc import ABCMeta

from typing import List

from connect.logger import logger, function_log
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Param
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from connect.models.tier_config import TierConfigRequest, TierConfigRequestSchema
from .automation import AutomationResource


class TierConfigAutomation(AutomationResource):
    __metaclass__ = ABCMeta
    resource = 'tier/config-requests'
    schema = TierConfigRequestSchema(many=True)

    def dispatch(self, request):
        # type: (TierConfigRequest) -> str
        try:
            if self.config.products \
                    and request.configuration.product.id not in self.config.products:
                return 'Invalid product'

            logger.info(
                'Start tier config request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            if not result:
                logger.info('Method `process_request` did not return result')
                return ''

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

        return ''

    @function_log
    def update_parameters(self, pk, params):
        # type: (str, List[Param]) -> str
        list_dict = []
        for _ in params:
            list_dict.append(_.__dict__ if isinstance(_, Param) else _)

        return self._api.put(
            path=pk,
            json={'params': list_dict},
        )[0]
