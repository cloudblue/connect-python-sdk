# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from abc import ABCMeta

from connect.models.usage import FileSchema
from connect.resource import AutomationResource


class UsageFileAutomation(AutomationResource):
    __metaclass__ = ABCMeta
    resource = 'usage/files'
    schema = FileSchema()
