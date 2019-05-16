# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from abc import ABCMeta

from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.logger import logger, function_log
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Param, \
    Fulfillment, TierConfigRequestSchema
from .automation_engine import AutomationEngine


class FulfillmentAutomation(AutomationEngine):
    """ This is the automation engine for the Fulfillment API.  If you want to process fulfillment
    requests, subclass this and implement the ``process_request`` method, which receives a
    :py:class:`connect.models.Fulfillment` request as argument and must return an
    :py:class:`ActivationTemplateResponse` or :py:class:`ActivationTileResponse` object in case
    the request has to be approved.

    In other case, you must raise one of these exceptions:

    - :py:class:`connect.models.InquireRequest`: Inquire for more information.
    - :py:class:`connect.models.FailRequest`: Causes the request to fail.
    - :py:class:`connect.models.SkipRequest`: Skips processing the request.

    Create an instance of your subclass and call its ``process`` method to begin processing.

    For an example on how to use this class, see :ref:`fulfillment_example`.
    """

    __metaclass__ = ABCMeta
    resource = 'requests'
    model_class = Fulfillment

    def filters(self, status='pending', **kwargs):
        """
        :param str status: Status of the requests. Default: ``'pending'``.
        :param dict[str,Any] kwargs: Additional filters to add to the default ones.
        :return: The set of filters for this resource.
        :rtype: dict[str,Any]
        """
        filters = super(FulfillmentAutomation, self).filters(status=status, **kwargs)
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

        except InquireRequest as inquire:
            self.update_parameters(request.id, inquire.params)
            return self.inquire(request.id)

        except FailRequest as fail:
            return self.fail(request.id, reason=fail.message)

        except SkipRequest as skip:
            return skip.code

    def get_tier_config(self, tier_id, product_id):
        """
        Gets the specified tier config data. For example, to get Tier 1 configuration data
        for one request, within the FulfillmentAutomation instance, we can do: ::

            self.get_tier_config(request.asset.tiers.tier1.id, request.asset.product.id)

        :param str tier_id: Id of the requested Tier Config.
        :param str product_id: Id of the product.
        :return: The requested Tier Config, or ``None`` if it was not found.
        :rtype: Optional[TierConfig]
        """
        url = self._api.urljoin(self.config.api_url, 'tier/config-requests')
        params = {
            'status': 'approved',
            'configuration__product__id': product_id,
            'configuration__account__id': tier_id,
        }
        response, _ = self._api.get(url=url, params=params)
        objects = self._load_schema(response, schema=TierConfigRequestSchema(many=True))

        if isinstance(objects, list) and len(objects) > 0:
            return objects[0].configuration
        else:
            return None

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
            json={'asset': {'params': list_dict}},
        )[0]
