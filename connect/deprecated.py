# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from functools import wraps
import inspect
import warnings

import six


def deprecated(new_name):
    if isinstance(new_name, six.string_types):
        # Called with a new name
        def top_decorator(func):
            @wraps(func)
            def func_wrap(*args, **kwargs):
                warnings.warn('Call to deprecated {type} `{name}` (Use `{new_name}` instead).'
                              .format(type='function' if inspect.isfunction(func) else 'class',
                                      name=func.__name__, new_name=new_name),
                              DeprecationWarning)
                return func(*args, **kwargs)

            return func_wrap

        return top_decorator

    elif inspect.isclass(new_name) or inspect.isfunction(new_name):
        # Called without new name
        @wraps(new_name)
        def decorator(*args, **kwargs):
            warnings.warn('Call to deprecated {type} `{name}`.'
                          .format(type='function' if inspect.isfunction(new_name) else 'class',
                                  name=new_name.__name__),
                          DeprecationWarning)
            return new_name(*args, **kwargs)

        return decorator

    else:
        raise TypeError(repr(type(new_name)))
