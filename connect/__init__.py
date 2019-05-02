# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from .resource import FulfillmentAutomation, TierConfigAutomation

name = 'connect'

__all__ = [
    'config',
    'logger',
    'migration_handler',
    'models',
    'resource',

    # TODO: Provided for backwards compatibility
    'FulfillmentAutomation',
    'TierConfigAutomation',
]
