# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from abc import ABCMeta

from connect.logger import logger, function_log
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Param, FailRequest,\
    InquireRequest, SkipRequest, TierConfigRequest, TierConfigRequestSchema
from .automation_engine import AutomationEngine


class TierConfigAutomation(AutomationEngine):
    """ This is the automation engine for the Tier Config Request API.  If you want to process
    Tier Config requests, subclass this and implement the ``process_request`` method,
    which receives a :py:class:`connect.models.TierConfigRequest` request as argument and must
    return an :py:class:`ActivationTemplateResponse` or :py:class:`ActivationTileResponse` object
    in case the request has to be approved.

    In other case, you must raise one of these exceptions:

    - :py:class:`connect.models.InquireRequest`: Inquire for more information.
    - :py:class:`connect.models.FailRequest`: Causes the request to fail.
    - :py:class:`connect.models.SkipRequest`: Skips processing the request.

    Create an instance of your subclass and call its ``process`` method to begin processing.
    """

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

        except InquireRequest as inquire:
            self.update_parameters(request.id, inquire.params)
            return self.inquire(request.id)

        except FailRequest as fail:
            return self.fail(request.id, reason=fail.message)

        except SkipRequest as skip:
            return skip.code

        return ''

    @function_log
    def update_parameters(self, pk, params):
        """ Sends a list of Param objects to Connect for updating.

        :param str pk: Id of the request.
        :param list[Param] params: List of parameters to update.
        :return: The server response.
        :rtype: str
        """
        list_dict = []
        for _ in params:
            list_dict.append(_.__dict__ if isinstance(_, Param) else _)

        return self._api.put(
            path=pk,
            json={'params': list_dict},
        )[0]
