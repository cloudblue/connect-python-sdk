# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import BillingSchema

class Billing(BaseModel):
    """ Billing object. """

    _schema = BillingSchema()

    stats = None  # type: Stats
    """ (:py:class:`.Stats`) Stats of companySchema. """

    period = None  # type: Period
    """ (:py:class:`.Period`) Period of the billing. """

    next_date = None  # type: str
    """ (str) Next date of the billing. """

    aniversary = None  # type: Aniversary
    """ (:py:class:`.Aniversary`) Aniversary. """
