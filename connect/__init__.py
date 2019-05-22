# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from .resources import FulfillmentAutomation, TierConfigAutomation

name = 'connect'

__all__ = [
    'config',
    'exceptions',
    'logger',
    'models',
    'resources',

    # TODO: Provided for backwards compatibility
    'FulfillmentAutomation',
    'TierConfigAutomation',
]
