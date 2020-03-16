# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

from abc import ABCMeta
import logging

from deprecation import deprecated
from typing import Optional

from connect.logger import function_log
from connect.models.tier_account import TierAccount
from connect.models.tier_account_request import TierAccountRequest
from connect.resources.automation_engine import AutomationEngine
from connect.resources.fulfillment import Fulfillment

class TierAccountRequestAutomation(AutomationEngine):
    """ This is the automation engine for the Tier Account Request API. If you want to process
    tier account request, subclass this and implement the ``process_request`` method, which receives a
    :py:class:`connect.models.tierAccountRequest` request as argument and must return an
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
    resource = 'tier/account-requests'
    model_class = TierAccountRequest
    logger = logging.getLogger('TierAccountRequest.logger')

    @function_log(custom_logger=logger)
    def dispatch(self, request):
        tier = Fulfillment(config=self.configuration)
        print('==============================')
        print(self.config.products)
        print('==============================')
        # print(tier.get_pending_tier_account_requests())
        print('==============================')


        '''
        if self.config.products \
            and request.asset.product.id not in self.config.products:
            self.logger.info('Invalid Product')
            return 'Invalid product'
        '''
        