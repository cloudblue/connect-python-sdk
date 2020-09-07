# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from abc import ABCMeta

from deprecation import deprecated
from typing import Optional

from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.logger import function_log
from connect.models.activation_template_response import ActivationTemplateResponse
from connect.models.activation_tile_response import ActivationTileResponse
from connect.models.asset_request import AssetRequest
from connect.models.param import Param
from connect.models.fulfillment import Fulfillment
from connect.models.tier_config_request import TierConfigRequest
from connect.models.conversation import Conversation
from connect.resources.automation_engine import AutomationEngine


class FulfillmentAutomation(AutomationEngine):
    """ This is the automation engine for the Fulfillment API.  If you want to process fulfillment
    requests, subclass this and implement the ``process_request`` method, which receives a
    :py:class:`connect.models.Fulfillment` request as argument and must return an
    :py:class:`connect.models.ActivationTemplateResponse` or
    :py:class:`connect.models.ActivationTileResponse` object in case the request has to be approved.

    In other case, you must raise one of these exceptions:

    - :py:class:`connect.exceptions.InquireRequest`: Inquire for more information.
    - :py:class:`connect.exceptions.FailRequest`: Causes the request to fail.
    - :py:class:`connect.exceptions.SkipRequest`: Skips processing the request.

    Create an instance of your subclass and call its ``process`` method to begin processing.

    For an example on how to use this class, see :ref:`fulfillment_example`.
    """

    __metaclass__ = ABCMeta
    resource = 'requests'
    model_class = Fulfillment

    def filters(self, status='pending', **kwargs):
        """ Returns the default set of filters for Fulfillment request, plus any others that you
        might specify. The allowed filters are:

        - status
        - created
        - id (List support)
        - type (purchase|renew|change|cancel)
        - asset.id (asset_id) - (List support)
        - asset.product.id (product_id)
        - asset.product.name - (List support)
        - asset.hub.id
        - asset.connection.hub.name - (List support)
        - asset.connection.provider.id
        - asset.connection.provider.name - (List support)
        - asset.connection.vendor.name - (List support)
        - asset.tiers.customer.id (Customer ID)
        - asset.tiers.tier1.id
        - asset.tiers.tier2.id
        - asset.connection.type (test|production|preview)

        :param str status: Status of the requests. Default: ``'pending'``.
        :param dict[str,Any] kwargs: Additional filters to add to the default ones.
        :return: The set of filters for this resource.
        :rtype: dict[str,Any]
        """
        query = super(FulfillmentAutomation, self).filters(status=status, **kwargs)
        if self.config.products:
            query.in_('asset.product.id', self.config.products)
        return query

    @function_log
    def dispatch(self, request):
        # type: (Fulfillment) -> str
        conversation = request.get_conversation(self.config)

        try:
            if self.config.products \
                    and request.asset.product.id not in self.config.products:
                return 'Invalid product'

            self.logger.info('Start request process / ID request - {}'.format(request.id))
            process_result = self.process_request(request)

            if not process_result:
                self.logger.info('Method `process_request` did not return result')
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

            self._update_conversation_if_exists(conversation, request.id, message)
            return approved

        except InquireRequest as inquire:
            self.update_parameters(request.id, inquire.params)
            inquired = self.inquire(request.id)
            self._update_conversation_if_exists(conversation, request.id, inquire)
            return inquired

        except FailRequest as fail:
            # PyCharm incorrectly detects unreachable code here, so disable
            # noinspection PyUnreachableCode
            failed = self.fail(request.id, reason=str(fail))
            self._update_conversation_if_exists(conversation, request.id, fail)
            return failed

        except SkipRequest as skip:
            self._update_conversation_if_exists(conversation, request.id, skip)
            return skip.code

        except NotImplementedError:
            raise

        except Exception as ex:
            self.logger.warning('Skipping request {} because an exception was raised: {}'
                                .format(request.id, ex))
            return ''

    def create_request(self, request):
        """ Creates a new request. Using this method requires a provider token used as api_key
        in the Config.

        :param Fulfillment request:
        :return: The created request.
        :rtype: Fulfillment
        """
        response, _ = self._api.post(json=request.json)
        return Fulfillment.deserialize(response)

    @deprecated(deprecated_in='16.0', details='Use ``TierConfig.get`` instead.')
    def get_tier_config(self, tier_id, product_id):
        """
        Gets the specified tier config data. For example, to get Tier 1 configuration data
        for one request, within the FulfillmentAutomation instance, we can do: ::

            self.get_tier_config(request.asset.tiers.tier1.id, request.asset.product.id)

        :param str tier_id: Account Id of the requested Tier Config (id with TA prefix).
        :param str product_id: Id of the product.
        :return: The requested Tier Config, or ``None`` if it was not found.
        :rtype: Optional[TierConfig]
        """
        url = self._api.urljoin(self.config.api_url, 'tier/config-requests')
        params = {
            'status': 'approved',
            'configuration.product.id': product_id,
            'configuration.account.id': tier_id,
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
        mapped_params = [p.json for p in params if isinstance(p, Param)]
        return self._api.put(
            path=pk,
            json={'asset': {'params': mapped_params}},
        )[0]

    def _update_conversation_if_exists(self, conversation, request_id, obj):
        # type: (Optional[Conversation], str, object) -> None
        if conversation:
            try:
                conversation.add_message(str(obj))
            except TypeError as ex:
                self.logger.error('Error updating conversation for request {}: {}'
                                  .format(request_id, ex))

    def _set_logger_prefix(self, request):
        # type: (Optional[AssetRequest]) -> None
        if request:
            self.logger.prefix = request.id
        else:
            self.logger.prefix = ''
