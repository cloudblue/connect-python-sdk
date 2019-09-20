# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import List

from .base import BaseModel
from .param import Param
from .schemas import ConfigurationSchema


class Configuration(BaseModel):
    """ Configuration Phase Parameter Context-Bound Data Object.

    To be used in parameter contexts:

    - Asset.
    - Fulfillment Request.
    - TierConfig.
    - TierConfig Requests.
    """

    _schema = ConfigurationSchema()

    params = None  # type: List[Param]
    """ (List[:py:class:`.Param`])  """
