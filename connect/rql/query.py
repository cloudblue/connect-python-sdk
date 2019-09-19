# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from typing import Dict


class Query(object):
    def __init__(self, properties=None):
        """
        The Query class allows you to specify filters using the
        `Resource Query Language <https://github.com/persvr/rql>`_ syntax.
        :param dict properties: Initial list of input properties
        """
        super(Query, self).__init__()
        self._in = []  # type: Dict[str, list]
        self._out = []  # type: Dict[str, list]
        self._limit = ''  # type: Dict[str, int]
        self._sort = []  # type: list
        self._like = []  # type: Dict[str, str]
        self._select = []  # type: list
        self._relationalOps = []  # type: Dict[str, list]

        if properties:
            for key, value in properties.items():
                if isinstance(value, list):
                    self.in_(key, value)
                else:
                    self.equal(key, value)

    def in_(self, prop, values):
        self._in[prop] = values
        return self

    def out(self, prop, values):
        self._out[prop] = values
        return self

    def limit(self, start, number):
        self._limit = {
            'start': start,
            'number': number
        }
        return self

    def sort(self, properties):
        self._sort = properties
        return self

    def like(self, prop, pattern):
        self._like[prop] = pattern
        return self

    def select(self, attributes):
        self._select = attributes
        return self

    def equal(self, prop, value):
        if 'eq' not in self._relationalOps:
            self._relationalOps['eq'] = []
        self._relationalOps['eq'].append([prop, value])
