# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import List

from .base import BaseModel
from .value_choice import ValueChoice
from .schemas import ConstraintsSchema


class Constraints(BaseModel):
    """ Parameter constraints. """

    _schema = ConstraintsSchema()

    hidden = None  # type: bool
    """ (bool) Is the parameter hidden? """

    required = None  # type: bool
    """ (bool) Is the parameter required? """

    choices = None  # type: List[ValueChoice]
    """ (List[:py:class:`.ValueChoice`]) Parameter value choices. """

    unique = None  # type: bool
    """ (bool) Is the constraint unique? """

    reconciliation = None  # type: bool
    """ (bool) True if vendor has marked parameters as for reconciliation purposes """

    min_length = None  # type: int
    """ (integer) Only for password type """

    max_length = None  # type: int
    """ (integer) Only for password type """
