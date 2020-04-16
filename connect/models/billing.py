# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import BillingSchema


class Billing(BaseModel):
    """ Billing object. """

    _schema = BillingSchema()

    stats = None  # type: object
    """ (:py:class:`.Stats`) BillingStats of companySchema. """

    period = None  # type: object
    """ (:py:class:`.Period`) Period of the billing. """

    next_date = None  # type: str
    """ (str) Next date of the billing. """

    anniversary = None  # type: object
    """ (:py:class:`.Anniversary`) Anniversary. """
