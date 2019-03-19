# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from .fulfillment_automation import FulfillmentAutomation
from .automation import AutomationResource
from .template import TemplateResource
from .tier_config_request_automation import TierConfigRequestAutomation


__all__ = [
    'FulfillmentAutomation',
    'AutomationResource',
    'TemplateResource',
    'TierConfigRequestAutomation',
]
