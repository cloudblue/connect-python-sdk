# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from connect.models.billing_request import BillingRequest
from .base import BaseResource


class BillingRequestResource(BaseResource):
    """ Billing Request Request Resource. """
    resource = 'subscriptions/requests'
    model_class = BillingRequest

    def update_billing_request(self, id_billing_request, body):
        """ Update Billing Request Attribute
        :param str id_billing_request: Primary key of the billing request to update.
        :param str body: Obj to update.
        :return: Billing Request Attributes Object.
        """
        if not id_billing_request:
            raise ValueError('Invalid ID')
        response = self._api.put(
            path='{}/attributes'.format(id_billing_request),
            json=body
            )
        return response
