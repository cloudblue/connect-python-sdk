# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import TierAccountRequestSchema


class TierAccountRequest(BaseModel):
    """ Tier account request. """
    _schema = TierAccountRequestSchema()

    type = None
    status = None
    account = None
    provider = None
    vendor = None
    product = None
    reason = None
    contact_info = None
    external_id = None
    external_uid = None
    events = None
