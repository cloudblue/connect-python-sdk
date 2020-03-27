# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import BillingRequestSchema

class BillingRequest(BaseModel):
    """ BillingRequest object. """

    _schema = BillingRequestSchema()

    type = None  # type: [str]
    """ (vendor|provider) Billing Request type. """

    events = None  # type: obj
    """ (obj) Billing Request Events. """

    asset = None  # type: obj
    """ (obj) Billing Request Asset. """

    item = None  # type: obj
    """ (obj) Billing Request Item. """

    asset = None  # type: obj
    """ (obj) Billing Request Asset. """

    period = None  # type: obj
    """ (obj) Billing Request Period. """
