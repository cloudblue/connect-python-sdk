# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from functools import wraps
import json
import logging
import os
from logging.config import dictConfig
from connect.models import BaseModel, Fulfillment

with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
    config = json.load(config_file)

dictConfig(config['logging'])

logger = logging.getLogger("Generic.logger")


def function_log(custom_logger=None):
    if not custom_logger:
        custom_logger = logging.getLogger()
        sformat = " %(levelname)-6s; %(asctime)s; %(name)-6s; %(module)s:%(funcName)s:line" \
                  "-%(lineno)d: %(message)s"
        [handler.setFormatter(logging.Formatter(sformat, "%I:%M:%S"))
         for handler in custom_logger.handlers]

    def real_function_log(func):
        @wraps(func)
        def decorator(self, *args, **kwargs):
            custom_logger.info('Entering: %s', func.__name__)
            custom_logger.debug('Function params: {} {}'.format(args, kwargs))
            result = func(self, *args, **kwargs)
            custom_logger.debug(
                'Function `{}.{}` return: {}'.format(self.__class__.__name__, func.__name__, result))
            return result

        return decorator
