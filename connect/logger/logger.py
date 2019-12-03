# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from functools import wraps
import json
import copy
import logging
import os
from logging.config import dictConfig

with open(os.path.join(os.path.dirname(__file__), 'config.json')) as config_file:
    config = json.load(config_file)

dictConfig(config['logging'])

logger = logging.getLogger()

DEFAULT_HIDDEN_REPLACEMENT = "**************"


def replace_dict_sensitive_data(elements, hidden_fields):
    for key, value in elements.items():
        if isinstance(value, dict):
            replace_dict_sensitive_data(value, hidden_fields)

        elements[key] = unpack_string_responses(value, hidden_fields) or elements[key]

        if key in hidden_fields:
            elements[key] = DEFAULT_HIDDEN_REPLACEMENT
    return elements


def replace_list_sensitive_data(elements, hidden_fields):
    working_elements = list(elements) if isinstance(elements, tuple) else elements
    for key, value in enumerate(working_elements):
        if isinstance(value, dict):
            replace_dict_sensitive_data(value, hidden_fields)
        working_elements[key] = unpack_string_responses(value, hidden_fields) or value
    return tuple(working_elements) if isinstance(elements, tuple) else working_elements


def unpack_string_responses(value, hidden_fields):
    if isinstance(value, str):
        try:
            parsed_value = json.loads(value)
            if isinstance(parsed_value, dict):
                return json.dumps(replace_dict_sensitive_data(parsed_value, hidden_fields))
            if isinstance(parsed_value, list) or isinstance(parsed_value, tuple):
                return json.dumps(replace_list_sensitive_data(parsed_value, hidden_fields))
        except ValueError:
            pass
    return None


def function_log(config=None, custom_logger=None):
    if not custom_logger:
        custom_logger = logging.getLogger()
        sformat = " %(levelname)-6s; %(asctime)s; %(name)-6s; %(module)s:%(funcName)s:line" \
                  "-%(lineno)d: %(message)s"
        for handler in custom_logger.handlers:
            handler.setFormatter(logging.Formatter(sformat, "%I:%M:%S"))
    hidden_fields = config.hidden_fields if config else []

    # noinspection PyUnusedLocal
    def decorator(func, **kwargs):
        # noinspection PyShadowingNames
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            custom_logger.info('Entering: %s', func.__name__)
            custom_logger.debug('Function params: {} {}'.format(
                replace_list_sensitive_data(copy.deepcopy(args), hidden_fields),
                replace_dict_sensitive_data({k: copy.deepcopy(v) for k, v in kwargs.items()}, hidden_fields)))
            result = func(self, *args, **kwargs)
            shown_result = replace_dict_sensitive_data(copy.deepcopy(result), hidden_fields) if isinstance(result, dict) \
                else replace_list_sensitive_data(copy.deepcopy(result), hidden_fields)
            custom_logger.debug(
                'Function `{}.{}` return: {}'.format(
                    self.__class__.__name__, func.__name__,
                    shown_result))
            return result

        return wrapper

    return decorator
