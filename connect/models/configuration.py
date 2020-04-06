# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

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

    def get_param_by_id(self, param_id):
        """ Get a parameter of the configuration.

        :param str param_id: Id of the the parameter to get.
        :return: The parameter with the given id, or ``None`` if it was not found.
        :rtype: :py:class:`.Param` | None
        """
        try:
            return list(filter(lambda param: param.id == param_id, self.params))[0]
        except IndexError:
            return None
