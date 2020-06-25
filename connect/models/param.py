# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import List, Optional

from .base import BaseModel
from .constraints import Constraints
from .events import Events
from .marketplace import Marketplace
from .value_choice import ValueChoice
from .schemas import ParamSchema


class Param(BaseModel):
    """ Parameters are used in product and asset definitions. """

    _schema = ParamSchema()

    name = None  # type: str
    """ (str) Name of parameter. """

    description = None  # type: str
    """ (str) Description of parameter. """

    type = None  # type: str
    """ (str) Type of parameter. """

    value = None  # type: Optional[str]
    """ (str|None) Value of parameter. """

    value_error = None  # type: Optional[str]
    """ (str|None) Error indicated for parameter. """

    value_choice = None  # type: Optional[List[str]]
    """ (List[str]|None) Available choices for parameter. """

    title = None  # type: Optional[str]
    """ (str|None) Title for parameter. """

    scope = None  # type: Optional[str]
    """ (str|None) Scope of parameter. """

    constraints = None  # type: Optional[Constraints]
    """ (:py:class:`.Constraints` | None) Parameter constraints. """

    value_choices = None  # type: Optional[List[ValueChoice]]
    """ (List[str]|None) Available dropdown choices for parameter. """

    structured_value = None  # type: Optional[dict]

    phase = None  # type: Optional[str]
    """ (str|None) Param phase. """

    events = None  # type: Optional[Events]
    """ (:py:class:`.Events` | None) Events. """

    marketplace = None  # type: Optional[Marketplace]
    """ (:py:class:`.Marketplace` | None) Marketplace. """

    reconciliation = None   # type: Optional[bool]
    """ (bool|None) Is Parameter used as reconciliation one from vendor invoices """
