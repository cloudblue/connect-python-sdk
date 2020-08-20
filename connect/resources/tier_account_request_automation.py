# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import logging

from connect.logger import function_log
from connect.resources.fulfillment import FulfillmentResource


class TierAccountRequestAction:
    """ This is the automation engine for the Tier Account Request API.  If you want to process
    Tier Account requests, subclass this and implement the ``process_request`` method,
    which receives a :py:class:`connect.models.TierAccountRequest` request as argument and returns
    a collection of Tier Account Request Object, this is processed calling to method dispatch and
    redirect to proccess_request.
    Create an instance of your subclass and call its ``process`` method to begin processing.
    The method process_request implements the business logic and depending of the evaluation,
    will invoque the methods ACCEPT, IGNORE or SKIP for each TAR.
    For an example on how to use this class, see :ref:`tier_account_example`.
    """
    ACCEPT = 'accept'
    IGNORE = 'ignore'
    SKIP = 'skip'

    def __init__(self, action, data=None):
        if action not in ('accept', 'ignore', 'skip'):
            raise Exception("Action no valid")
        self._action = action
        self._data = data

    @property
    def action(self):
        return self._action

    @property
    def data(self):
        return self._data


class TierAccountRequestAutomation:
    logger = logging.getLogger(__name__)

    def __init__(self, config):
        self.config = config
        self.fulfillment = FulfillmentResource(config=self.config)

    def process(self, filters=None):
        for request in self.fulfillment.search_tier_account_requests(
                filters or dict(status='pending')
        ):
            self.dispatch(request)

    @function_log
    def dispatch(self, request):
        result = self.process_request(request)
        if result.action == TierAccountRequestAction.ACCEPT:
            self.fulfillment.accept_tier_account_request(request.id)
        if result.action == TierAccountRequestAction.IGNORE:
            self.fulfillment.ignore_tier_account_request(request.id, result.data)
        if result.action == TierAccountRequestAction.SKIP:
            pass

    def process_request(self, request):
        raise NotImplementedError('Please implement `{}.process_request` method'
                                  .format(self.__class__.__name__))
