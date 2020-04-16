# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import datetime
from typing import Optional

from .activation import Activation
from .agreement import Agreement
from .base import BaseModel
from .company import Company
from .marketplace import Marketplace
from .user import User
from .schemas import ContractSchema


class Contract(BaseModel):
    """ Contract object. """

    _schema = ContractSchema()

    name = None  # type: str
    """ (str) Contract name. """

    version = None  # type: int
    """ (int) Version of the contract (same as associated agreement version). """

    type = None  # type: str
    """ (str) Type of the contract (same as agreement type). One of:
    distribution, program, service.
    """

    status = None  # type: str
    """ (str) Contract Status. One of: enrolling, pending, active, terminated, rejected """

    agreement = None  # type: Agreement
    """ (:py:class:`.Agreement`) Reference object to the agreement. """

    marketplace = None  # type: Optional[Marketplace]
    """ (:py:class:`.Marketplace` | None) Reference object to the agreement marketplace. """

    owner = None  # type: Optional[Company]
    """ (:py:class:`.Company` | None) Reference object to the owner company. """

    creator = None  # type: User
    """ (:py:class:`.User`) Reference object to the creator. """

    created = None  # type: datetime.datetime
    """ (datetime.datetime) Contract creation date. """

    updated = None  # type: datetime.datetime
    """ (datetime.datetime) Date of contract status update. """

    enrolled = None  # type: Optional[datetime.datetime]
    """ (datetime.datetime|None) Date when contract was enrolled. """

    version_created = None  # type: datetime.datetime
    """ (datetime.datetime) Contract version creation date. """

    activation = None  # type: Activation
    """ (:py:class:`.Activation`) Activation information. """

    signee = None  # type: Optional[User]
    """ (:py:class:`.User` | None) Reference object to the user of the owner company,
    who signed the contract.
    """
