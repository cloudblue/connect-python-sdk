# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import datetime
from typing import Optional, List

from .agreement_stats import AgreementStats
from .base import BaseModel
from .company import Company
from .marketplace import Marketplace
from .user import User
from .schemas import AgreementSchema


class Agreement(BaseModel):
    """ An Agreement object. """

    _schema = AgreementSchema()

    type = None  # type: str
    """ (str) Type of the agreement. One of: distribution, program, service. """

    title = None  # type: str
    """ (str) Title of the agreement. """

    description = None  # type: str
    """ (str) Agreement details (Markdown). """

    created = None  # type: datetime.datetime
    """ (datetime.datetime) Date of creation of the agreement. """

    updated = None  # type: datetime.datetime
    """ (datetime.datetime) Date of the update of the agreement. It can be creation
    of the new version, change of the field, etc. (any change).
    """

    owner = None  # type: Company
    """ (:py:class:`.Company`) Reference to the owner account object. """

    stats = None  # type: Optional[AgreementStats]
    """ (:py:class:`.AgreementStats` | None) Agreement stats. """

    author = None  # type: Optional[User]
    """ (:py:class:`.User` | None) Reference to the user who created the version. """

    version = None  # type: int
    """ (int) Chronological number of the version. """

    active = None  # type: bool
    """ (bool) State of the version. """

    link = None  # type: str
    """ (str) Url to the document. """

    version_created = None  # type: datetime.datetime
    """ (datetime.datetime) Date of the creation of the version. """

    version_contracts = None  # type: int
    """ (int) Number of contracts this version has. """

    agreements = None  # type: List[Agreement]
    """ (List[:py:class:`.Agreement`]) Program agreements can have distribution agreements
    associated with them.
    """

    parent = None  # type: Optional[Agreement]
    """ (:py:class:`.Agreement` | None) Reference to the parent program agreement
    (for distribution agreement).
    """

    marketplace = None  # type: Optional[Marketplace]
    """ (:py:class:`.Marketplace` | None) Reference to marketplace object
    (for distribution agreement).
    """

    # Undocumented fields (they appear in PHP SDK)

    name = None  # type: str
    """ (str) Name of Agreement. """
