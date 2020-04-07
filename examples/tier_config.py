# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

# NOTE: This example development is in progress. This is just a skeleton.

from typing import Union
import warnings

from connect.config import Config
from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse, TierConfigRequest
from connect.resources import TierConfigAutomation

# Enable processing of deprecation warnings
warnings.simplefilter('default')

# Set logger level / default level ERROR
logger.setLevel('DEBUG')

# If we remove this line, it is done implicitly
Config(file='./examples/config.json')


class TierConfigExample(TierConfigAutomation):

    def process_request(self, request):
        # type: (TierConfigRequest) -> Union[ActivationTemplateResponse, ActivationTileResponse]
        pass


if __name__ == '__main__':
    tier_config_example = TierConfigExample()
    tier_config_example.process()
