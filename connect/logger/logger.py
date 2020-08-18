# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from functools import wraps
import json
import logging
import os
from logging.config import dictConfig

with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
    config = json.load(config_file)

dictConfig(config['logging'])

logger = logging.getLogger()


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger_):
        super(LoggerAdapter, self).__init__(logger_, {})
        self.prefix = None

    def process(self, msg, kwargs):
        return (
            '[%s] %s' % (self.prefix, msg) if self.prefix else msg,
            kwargs
        )


def function_log(custom_logger=None):
    if not custom_logger:
        custom_logger = logging.getLogger()
        sformat = " %(levelname)-6s; %(asctime)s; %(name)-6s; %(module)s:%(funcName)s:line" \
                  "-%(lineno)d: %(message)s"
        for handler in custom_logger.handlers:
            handler.setFormatter(logging.Formatter(sformat))

    # noinspection PyUnusedLocal
    def decorator(func, **kwargs):
        # noinspection PyShadowingNames
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            custom_logger.info('Entering: %s', func.__name__)
            custom_logger.debug('Function params: {} {}'.format(args, kwargs))
            result = func(self, *args, **kwargs)
            custom_logger.debug(
                u'Function `{}.{}` return: {}'.format(
                    self.__class__.__name__, func.__name__, result))
            return result

        return wrapper

    return decorator
