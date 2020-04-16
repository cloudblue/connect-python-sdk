# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from connect.models.recurring_asset import RecurringAsset
from .base import BaseResource


class RecurringAssetResource(BaseResource):
    """ Recurring Asset Request Resource. """
    resource = 'subscriptions/assets'
    model_class = RecurringAsset
