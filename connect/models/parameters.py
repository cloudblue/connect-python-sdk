# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import List, Optional

from .base import BaseModel
from connect.models.schemas import ValueChoiceSchema, ConstraintsSchema, ParamSchema


class ValueChoice(BaseModel):
    """ A value choice for a parameter. """

    _schema = ValueChoiceSchema()

    value = None  # type: str
    """ (str) Value. """

    label = None  # type: str
    """ (str) Label. """


class Constraints(BaseModel):
    """ Parameter constraints. """

    _schema = ConstraintsSchema()

    hidden = None  # type: bool
    """ (bool) Is the parameter hidden? """

    required = None  # type: bool
    """ (bool) Is the parameter required? """

    choices = None  # type: List[ValueChoice]
    """ (List[:py:class:`.ValueChoice`]) Parameter value choices. """


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

    # Undocumented fields (they appear in PHP SDK)
    title = None  # type: Optional[str]
    """ (str|None) Title for parameter. """

    scope = None  # type: Optional[str]
    """ (str|None) Scope of parameter. """

    constraints = None  # type: Optional[Constraints]
    """ (:py:class:`.Constraints` | None) Parameter constraints. """
