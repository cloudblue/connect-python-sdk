# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import BillingRequestSchema


class BillingRequest(BaseModel):
    """ BillingRequest object. """

    _schema = BillingRequestSchema()

    type = None  # type: [str]
    """ (vendor|provider) Billing Request type. """

    events = None  # type: object
    """ (object) Billing Request Events. """

    asset = None  # type: object
    """ (object) Billing Request Asset. """

    item = None  # type: object
    """ (object) Billing Request Item. """

    attrubutes = None  # type: object
    """ (object) Billing Request Attributes. """

    period = None  # type: object
    """ (object) Billing Request Period. """
