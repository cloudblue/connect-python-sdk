# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from abc import ABCMeta

from typing import Dict, Any

from connect.models.usage import FileSchema, Listing
from connect.resource import AutomationResource


class UsageAutomation(AutomationResource):
    __metaclass__ = ABCMeta
    resource = 'usage/files'
    schema = FileSchema()

    def build_filter(self, status='listed'):
        # type: (str) -> Dict[str, Any]
        return super(UsageAutomation, self).build_filter(status=status)

    def dispatch(self, request):
        # type: (Listing) -> str
        pass
