# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from abc import ABCMeta

from deprecation import deprecated

from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.logger import logger, function_log
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Param, \
    Fulfillment, TierConfigRequest
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

        conversation = request.get_conversation(self.config)

        try:
            if self.config.products \
                    and request.asset.product.id not in self.config.products:
                return 'Invalid product'

            logger.info('Start request process / ID request - {}'.format(request.id))
            process_result = self.process_request(request)

            if not process_result:
                logger.info('Method `process_request` did not return result')
                return ''

            if isinstance(process_result, ActivationTileResponse):
                message = 'Activated using custom activation tile.'
                approved = self.approve(request.id, {'activation_tile': process_result.tile})
            elif isinstance(process_result, ActivationTemplateResponse):
                message = 'Activated using template {}.'.format(process_result.template_id)
                approved = self.approve(request.id, {'template_id': process_result.template_id})
            else:
                # We should not get here
                message = ''
                approved = ''

            if conversation:
                try:
                    conversation.add_message(message)
                except TypeError as ex:
                    logger.error('Error updating conversation for request {}: {}'
                                 .format(request.id, ex))
            return approved

        except InquireRequest as inquire:
            self.update_parameters(request.id, inquire.params)
            inquired = self.inquire(request.id)
            if conversation:
                try:
                    conversation.add_message(str(inquire))
                except TypeError as ex:
                    logger.error('Error updating conversation for request {}: {}'
                                 .format(request.id, ex))
            return inquired

        except FailRequest as fail:
            # PyCharm incorrectly detects unreachable code here, so disable
            # noinspection PyUnreachableCode
            failed = self.fail(request.id, reason=str(fail))
            if conversation:
                try:
                    conversation.add_message(str(fail))
                except TypeError as ex:
                    logger.error('Error updating conversation for request {}: {}'
                                 .format(request.id, ex))
            return failed

        except SkipRequest as skip:
            skipped = skip.code
            if conversation:
                try:
                    conversation.add_message(str(skip))
                except TypeError as ex:
                    logger.error('Error updating conversation for request {}: {}'
                                 .format(request.id, ex))
            return skipped

    @deprecated(deprecated_in='16.0', details='Use ``TierConfig.get`` instead.')
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
        objects = TierConfigRequest.deserialize(response)

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
