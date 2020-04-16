# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from abc import ABCMeta

from deprecation import deprecated

from .resources import FulfillmentAutomation as BaseFulfillmentAutomation
from .resources import TierConfigAutomation as BaseTierConfigAutomation


# TODO: These classes will be removed in the future.
# They are now located in connect.resources package.


class FulfillmentAutomation(BaseFulfillmentAutomation):
    __metaclass__ = ABCMeta

    @deprecated(deprecated_in='16.0',
                details='Import class from ``connect.resources`` package instead.')
    def __init__(self, config=None):
        super(FulfillmentAutomation, self).__init__(config)


class TierConfigAutomation(BaseTierConfigAutomation):
    __metaclass__ = ABCMeta

    @deprecated(deprecated_in='16.0',
                details='Import class from ``connect.resources`` package instead.')
    def __init__(self, config=None):
        super(TierConfigAutomation, self).__init__(config)


name = 'connect'


__all__ = [
    'FulfillmentAutomation',
    'TierConfigAutomation'
]
