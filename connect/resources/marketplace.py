# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseResource
from ..models import Marketplace


class MarketplaceResource(BaseResource):
    """ Resource to work with :py:class:`connect.models.Marketplace` models.
        :param Config config: Config object or ``None`` to use environment config (default).
    """
    resource = 'marketplaces'
    model_class = Marketplace

    def __init__(self, config=None):
        super(MarketplaceResource, self).__init__(config)
