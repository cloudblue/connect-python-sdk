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


class LoggerAdapterObserver(object):
    def on_begin_log(self, level, msg, *args, **kwargs):
        pass

    def on_end_log(self, level, msg, *args, **kwargs):
        pass


class LoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger_, extra=None, observer=None):
        super(LoggerAdapter, self).__init__(logger_, extra or {})
        self.prefix = None
        self.replace_handler = None
        self.observer = observer

    def process(self, msg, kwargs):
        if self.replace_handler:
            handlers_copy = self.logger.handlers[:]
            for handler in handlers_copy:
                if isinstance(handler, type(self.replace_handler)):
                    self.logger.removeHandler(handler)
                    self.logger.addHandler(self.replace_handler)
        msg, kwargs = super(LoggerAdapter, self).process(msg, kwargs)
        return (
            '%s %s' % (self.prefix, msg) if self.prefix else msg,
            kwargs
        )

    def debug(self, msg, *args, **kwargs):
        if self.observer:
            self.observer.on_begin_log(logging.DEBUG, msg, *args, **kwargs)
        try:
            super(LoggerAdapter, self).debug(msg, *args, **kwargs)
        finally:
            if self.observer:
                self.observer.on_end_log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.observer:
            self.observer.on_begin_log(logging.INFO, msg, *args, **kwargs)
        try:
            super(LoggerAdapter, self).info(msg, *args, **kwargs)
        finally:
            if self.observer:
                self.observer.on_end_log(logging.INFO, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.observer:
            self.observer.on_begin_log(logging.ERROR, msg, *args, **kwargs)
        try:
            super(LoggerAdapter, self).error(msg, *args, **kwargs)
        finally:
            if self.observer:
                self.observer.on_end_log(logging.ERROR, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        if self.observer:
            self.observer.on_begin_log(logging.ERROR, msg, *args, **kwargs)
        try:
            super(LoggerAdapter, self).exception(msg, *args, **kwargs)
        finally:
            if self.observer:
                self.observer.on_end_log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.observer:
            self.observer.on_begin_log(logging.CRITICAL, msg, *args, **kwargs)
        try:
            super(LoggerAdapter, self).critical(msg, *args, **kwargs)
        finally:
            if self.observer:
                self.observer.on_end_log(logging.CRITICAL, msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        if self.observer:
            self.observer.on_begin_log(level, msg, *args, **kwargs)
        try:
            super(LoggerAdapter, self).log(msg, *args, **kwargs)
        finally:
            if self.observer:
                self.observer.on_end_log(level, msg, *args, **kwargs)

    def setLevel(self, level):
        self.logger.setLevel(level)


def function_log(func):
    # noinspection PyShadowingNames
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        logger.debug('Entering: %s', func.__name__)
        logger.debug('Function params: {} {}'.format(args, kwargs))
        result = func(self, *args, **kwargs)
        logger.debug(u'Function `{}.{}` return: {}'
                     .format(self.__class__.__name__, func.__name__, result))
        return result
    return wrapper
