# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from abc import ABCMeta
from typing import Optional

from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.logger import function_log
from connect.models.activation_template_response import ActivationTemplateResponse
from connect.models.activation_tile_response import ActivationTileResponse
from connect.models.param import Param
from connect.models.tier_config_request import TierConfigRequest
from .automation_engine import AutomationEngine


class TierConfigAutomation(AutomationEngine):
    """ This is the automation engine for the Tier Config Request API.  If you want to process
    Tier Config requests, subclass this and implement the ``process_request`` method,
    which receives a :py:class:`connect.models.TierConfigRequest` request as argument and must
    return an :py:class:`connect.models.ActivationTemplateResponse` or
    :py:class:`connect.models.ActivationTileResponse` object in case the request has to be approved.

    In other case, you must raise one of these exceptions:

    - :py:class:`connect.exceptions.InquireRequest`: Inquire for more information.
    - :py:class:`connect.exceptions.FailRequest`: Causes the request to fail.
    - :py:class:`connect.exceptions.SkipRequest`: Skips processing the request.

    Create an instance of your subclass and call its ``process`` method to begin processing.

    For an example on how to use this class, see :ref:`tier_config_example`.
    """

    __metaclass__ = ABCMeta
    resource = 'tier/config-requests'
    model_class = TierConfigRequest

    def filters(self, status='pending', **kwargs):
        """ Returns the default set of filters for Tier Config request, plus any others that you
        might specify. The allowed filters are:

        - type
        - status
        - id
        - configuration.id
        - configuration.tier_level
        - configuration.account.id
        - configuration.product.id
        - assignee.id
        - unassigned (bool)
        - configuration.account.external_uid

        :param str status: Status of the requests. Default: ``'pending'``.
        :param dict[str,Any] kwargs: Additional filters to add to the default ones.
        :return: The set of filters for this resource.
        :rtype: dict[str,Any]
        """
        query = super(TierConfigAutomation, self).filters(status=status, **kwargs)
        if self.config.products:
            query.in_('configuration.product.id', self.config.products)
        return query

    @function_log
    def dispatch(self, request):
        # type: (TierConfigRequest) -> str
        try:
            if self.config.products \
                    and request.configuration.product.id not in self.config.products:
                return 'Invalid product'

            self.logger.info(
                'Start tier config request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            if not result:
                self.logger.info('Method `process_request` did not return result')
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
            return self.fail(request.id, reason=str(fail))

        except SkipRequest as skip:
            return skip.code

        except NotImplementedError:
            raise

        except Exception as ex:
            self.logger.warning('Skipping request {} because an exception was raised: {}'
                                .format(request.id, ex))
            return ''

        return ''

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
            json={'params': mapped_params},
        )[0]

    def _set_logger_prefix(self, request):
        # type: (Optional[TierConfigRequest]) -> None
        if request:
            self.logger.prefix = request.id + ' - ' + request.configuration.account.id
        else:
            self.logger.prefix = ''
