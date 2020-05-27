# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from connect.models import AssetRequest
from .base import BaseResource


class AssetRequestResource(BaseResource):
    """ Asset Request Resource. """
    resource = 'requests'
    model_class = AssetRequest

    def update_param_asset_request(self, request_id, data, note):
        """ Update Asset Request param
        :param str id_request: Primary key of the request to update.
        :param str data: params to update.
            {
                "params": [{
                    "id": "PM-9861-7949-8492-0001",
                    "value": "32323323"
                }]
            }
        :return: Asset Request Attributes Object.
        """
        if not request_id:
            raise ValueError('Invalid ID')
        body = {"note": note, "asset": data}
        response = self._api.put(
            path='{}/'.format(request_id),
            json=body
        )
        return response
