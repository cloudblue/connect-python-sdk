# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from connect.models.tier_config import TierConfig
from connect.models.tier_config_request import TierConfigRequest

from .base import BaseResource


class TierConfigResource(BaseResource):
    """ Tier Config Resource. """
    resource = 'tier/configs'
    model_class = TierConfig


class TierConfigRequestResource(BaseResource):
    """ Tier Config Request Resource. """
    resource = 'tier/config-requests'
    model_class = TierConfigRequest

    def pend(self, id_tcr):
        """ Set a Tier Configuration Request to pend status.
        :param str id_tar: Primary key of the tier configuration request to set.
        :return: 204, Empty response
        """
        if not id_tcr:
            raise ValueError('Invalid ID')
        response = self._api.post(path='{}/pend'.format(id_tcr))
        return response

    def inquire(self, id_tcr):
        """ Set a Tier Configuration Request to inquire status.
        :param str id_tar: Primary key of the tier configuration request to set.
        :return: 204, Empty response
        """
        if not id_tcr:
            raise ValueError('Invalid ID')
        response = self._api.post(path='{}/inquire'.format(id_tcr))
        return response

    def approve(self, tcr_id, template_id=None):
        """ Approve a Tier Configuration Request
        :param str tcr_id: Primary key of the tier configuration request to approve.
        :param str template_id: Primary key of the template.
        :return: Template object.
        """
        if not tcr_id:
            raise ValueError('Invalid ID')
        request_kwargs = {
            'path': '{}/approve'.format(tcr_id)
        }
        if template_id:
            request_kwargs['json'] = {
                'template': {
                    'id': template_id
                }
            }
        response = self._api.post(**request_kwargs)
        return response

    def fail(self, id_tcr, reason):
        """ Set fail a Tier Configuration Request
        :param str id_tar: Primary key of the tier configuration request to ignore.
        :param str reason: Reason of the fail.
        :return: 204, Empty response
        """
        if not id_tcr:
            raise ValueError('Invalid ID')
        response = self._api.post(
            path='{}/fail'.format(id_tcr),
            json={
                'reason': reason,
            })
        return response

    def assign(self, id_tcr):
        """ Assign a Tier Configuration Request.
        :param str id_tar: Primary key of the tier configuration request to set.
        :return: 204, Empty response
        """
        if not id_tcr:
            raise ValueError('Invalid ID')
        response = self._api.post(path='{}/assign'.format(id_tcr))
        return response

    def unassign(self, id_tcr):
        """ Unassign a Tier Configuration Request.
        :param str id_tar: Primary key of the tier configuration request to set.
        :return: 204, Empty response
        """
        if not id_tcr:
            raise ValueError('Invalid ID')
        response = self._api.post(path='{}/unassign'.format(id_tcr))
        return response
