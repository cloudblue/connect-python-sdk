# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from copy import copy
from typing import Dict, List, Optional


class Query(object):
    """
    The Query class allows you to specify filters using the
    `Resource Query Language <https://github.com/persvr/rql>`_ syntax.

    :param dict properties: Initial list of input properties
    """

    def __init__(self, properties=None):
        super(Query, self).__init__()
        self._in = {}  # type: Dict[str, List[str]]
        self._out = {}  # type: Dict[str, List[str]]
        self._limit = None  # type: Optional[int]
        self._order_by = None  # type: Optional[str]
        self._offset = None  # type: Optional[int]
        self._ordering = None  # type: Optional[List[str]]
        self._like = {}  # type: Dict[str, str]
        self._ilike = {}  # type: Dict[str, str]
        self._select = None  # type: Optional[List[str]]
        self._rel_ops = {}  # type: Dict[str, List[Dict[str, str]]]

        if properties:
            for key, value in properties.items():
                if hasattr(self, '_' + key):
                    setattr(self, '_' + key, value)
                elif isinstance(value, list):
                    self.in_(key, value)
                else:
                    self.equal(key, value)

    def in_(self, prop, values):
        """
        Select objects where the specified property value is in the provided array.

        :param str prop: Property
        :param list values: Values
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        self._in[prop] = copy(values)
        return self

    def out(self, prop, values):
        """
        Select objects where the specified property value is not in the provided array.

        :param str prop: Property
        :param list values: Values
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        self._out[prop] = copy(values)
        return self

    def limit(self, amount):
        """
        Indicates the given number of objects from the start position.

        :param int amount: Amount of objects to return.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        self._limit = amount
        return self

    def order_by(self, prop):
        """
        Order list by given property.

        :param str prop: Property.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        self._order_by = prop
        return self

    def offset(self, page):
        """
        Offset (page) to return on paged queries.

        :param int page: Offset.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        self._offset = page
        return self

    def ordering(self, props):
        """
        Order list of objects by the given properties (unlimited number of properties).
        The list is ordered first by the first specified property, then by the second, and
        so on. The order is specified by the prefix: + ascending order, - descending.

        :param list props: Properties.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        self._ordering = copy(props)
        return self

    def like(self, prop, pattern):
        """
        Search for the specified pattern in the specified property. The function is similar
        to the SQL LIKE operator, though it uses the * wildcard instead of %. To specify in
        a pattern the * symbol itself, it must be percent-encoded, that is, you need to specify
        %2A instead of *, see the usage examples below. In addition, it is possible to use the
        ? wildcard in the pattern to specify that any symbol will be valid in this position.

        :param str prop: Property.
        :param str pattern: Pattern.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        self._like[prop] = pattern
        return self

    def ilike(self, prop, pattern):
        """
        Same as like but case unsensitive.

        :param str prop: Property.
        :param str pattern: Pattern.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        self._ilike[prop] = pattern
        return self

    def select(self, attributes):
        """
        The function is applicable to a list of resources (hereafter base resources). It receives
        the list of attributes (up to 100 attributes) that can be primitive properties of the base
        resources, relation names, and relation names combined with properties of related
        resources. The output is the list of objects presenting the selected properties and related
        (linked) resources. Normally, when relations are selected, the base resource properties are
        also presented in the output.

        :param list attributes: Attributes.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        self._select = copy(attributes)
        return self

    def equal(self, prop, value):
        """
        Select objects with a property value equal to value.

        :param str prop: Property.
        :param str value: Value.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        return self._add_rel_op('eq', prop, value)

    def not_equal(self, prop, value):
        """
        Select objects with a property value not equal to value.

        :param str prop: Property.
        :param str value: Value.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        return self._add_rel_op('ne', prop, value)

    def greater(self, prop, value):
        """
        Select objects with a property value greater than the value.

        :param str prop: Property.
        :param str value: Value.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        return self._add_rel_op('gt', prop, value)

    def greater_equal(self, prop, value):
        """
        Select objects with a property value equal or greater than the value.

        :param str prop: Property.
        :param str value: Value.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        return self._add_rel_op('ge', prop, value)

    def lesser(self, prop, value):
        """
        Select objects with a property value less than the value.

        :param str prop: Property.
        :param str value: Value.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        return self._add_rel_op('lt', prop, value)

    def lesser_equal(self, prop, value):
        """
        Select objects with a property value equal or lesser than the value.

        :param str prop: Property.
        :param str value: Value.
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        return self._add_rel_op('le', prop, value)

    def compile(self):
        """
        :return: A string representation of the query.
        :rtype: str
        """
        rql = []

        if self._select:
            rql.append('select({})'.format(','.join(self._select)))

        for key, val in self._like.items():
            rql.append('like({},{})'.format(key, val))

        for key, val in self._ilike.items():
            rql.append('ilike({},{})'.format(key, val))

        for key, val in self._in.items():
            rql.append('in({},({}))'.format(key, ','.join(val)))

        for key, val in self._out.items():
            rql.append('out({},({}))'.format(key, ','.join(val)))

        for op, arguments in self._rel_ops.items():
            for argument in arguments:
                rql.append('{}({},{})'.format(op, argument['key'], argument['value']))

        if self._ordering:
            rql.append('ordering({})'.format(','.join(self._ordering)))

        if self._limit:
            rql.append('limit=' + str(self._limit))

        if self._order_by:
            rql.append('order_by=' + str(self._order_by))

        if self._offset:
            rql.append('offset=' + str(self._offset))

        return ('?' + '&'.join(rql)) if rql else ''

    def _add_rel_op(self, op, prop, value):
        """
        :param str op:
        :param str prop:
        :param str value:
        :return: The Query object to provide a fluent interface (chaining method calls).
        :rtype: :py:class:`.Query`
        """
        if op not in self._rel_ops:
            self._rel_ops[op] = []
        self._rel_ops[op].append({'key': prop, 'value': value})
        return self

    def __str__(self):
        return self.compile()
