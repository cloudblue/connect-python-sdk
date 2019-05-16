# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from functools import wraps
import inspect
import warnings


def deprecated(version, new_name):
    def decorator(func):
        @wraps(func)
        def func_wrap(*args, **kwargs):
            warnings.warn('Call to {type} `{name}` was deprecated in v{version} {usage}'
                          .format(type='function' if inspect.isfunction(func) else 'class',
                                  name=func.__name__,
                                  version=version,
                                  usage='(Use `{}` instead)'.format(new_name) if new_name else ''
                                  ), DeprecationWarning)
            return func(*args, **kwargs)

        return func_wrap

    return decorator
