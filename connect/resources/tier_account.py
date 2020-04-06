# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from connect.models.tier_account import TierAccount
from connect.models.tier_account_request import TierAccountRequest

from .base import BaseResource


class TierAccountResource(BaseResource):
    """ Tier Account Resource. """

    resource = 'tier/accounts'
    model_class = TierAccount


class TierAccountRequestResource(BaseResource):
    """ Tier Account Request Resource. """
    resource = 'tier/account-requests'
    model_class = TierAccountRequest

    def accept(self, id_tar):
        """ Accept a Tier Configuration Request.
        :param str id_tar: Primary key of the tier configuration request to accept.
        :return: Tier Account Request object.
        """
        if not id_tar:
            raise ValueError('Invalid ID')
        response, _ = self._api.post(path='{}/accept'.format(id_tar))
        return self.model_class.deserialize(response)

    def ignore(self, id_tar, reason):
        """ Ignore a Tier Configuration Request
        :param str id_tar: Primary key of the tier configuration request to ignore.
        :return: Tier Account Request object.
        """
        if not id_tar:
            raise ValueError('Invalid ID')
        response, _ = self._api.post(
            path='{}/ignore'.format(id_tar),
            json={
                'reason': reason,
            })
        return self.model_class.deserialize(response)
