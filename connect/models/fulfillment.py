# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from deprecation import deprecated

from .asset_request import AssetRequest
from .schemas import FulfillmentSchema


class Fulfillment(AssetRequest):
    """ Represents a request for the :py:class:`connect.resource.FulfillmentAutomation`
    resource.
    """
    _schema = FulfillmentSchema()

    @deprecated(deprecated_in='19.2',
                details='Use `connect.models.AssetRequest` instead.')
    def __init__(self, *args, **kwargs):
        super(Fulfillment, self).__init__(*args, **kwargs)
