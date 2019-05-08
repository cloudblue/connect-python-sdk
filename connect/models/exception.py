# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

# This file provides backwards compatibility with the previous location
# and names of exception classes
# TODO: Add deprecation warning

from connect.exceptions import FailRequest as FulfillmentFail
from connect.exceptions import InquireRequest as FulfillmentInquire
from connect.exceptions import SkipRequest as Skip

__all__ = [
    'FulfillmentFail',
    'FulfillmentInquire',
    'Skip'
]
