# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from abc import ABCMeta

from connect.exceptions import FailRequest, InquireRequest, SkipRequest
from connect.logger import logger, function_log
from connect.models import ActivationTemplateResponse, ActivationTileResponse, Param, \
    TierConfigRequest
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
            return self.fail(request.id, reason=str(fail))

        except SkipRequest as skip:
            return skip.code

        except NotImplementedError:
            raise

        except Exception as ex:
            logger.warning('Skipping request {} because an exception was raised: {}'
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
        list_dict = []
        for _ in params:
            list_dict.append(_.__dict__ if isinstance(_, Param) else _)

        return self._api.put(
            path=pk,
            json={'params': list_dict},
        )[0]
