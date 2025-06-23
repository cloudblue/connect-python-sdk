# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import CompanySchema


class Company(BaseModel):
    """ Represents a company within the platform. """

    _schema = CompanySchema()

    name = None  # type: str
    """ (str) Company name. """

    last_request = None  # type: object
    """ (:py:class:`.LastRequest`) Last Request of companySchema. """

    count = None  # type: int
    """ (integer) Count. """
