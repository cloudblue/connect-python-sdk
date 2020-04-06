# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from connect.rql import Query


def test_empty_initializer():
    rql = Query()
    assert rql.compile() == ''


def test_initializer_1():
    rql = Query({
        'product.id': 'PRD-123123123',
        'ordering': ['test1', 'test2'],
        'limit': 10,
        'offset': 4,
        'order_by': 'property'
    })
    assert rql.compile() == '?eq(product.id,PRD-123123123)&ordering(test1,test2)&limit=10'\
                            '&order_by=property&offset=4'


def test_initializer_2():
    rql = Query({
        'product.id': ['PRD-123123123', 'PRD-123123123']
    })
    assert rql.compile() == '?in(product.id,(PRD-123123123,PRD-123123123))'


def test_equal():
    rql = Query().equal('key', 'value')
    assert rql.compile() == '?eq(key,value)'


def test_not_equal():
    rql = Query().not_equal('property', 'value')
    assert rql.compile() == '?ne(property,value)'


def test_in():
    rql = Query().in_('key', ['value1', 'value2'])
    assert rql.compile() == '?in(key,(value1,value2))'


def test_out():
    rql = Query().out('product.id', ['PR-', 'CN-'])
    assert rql.compile() == '?out(product.id,(PR-,CN-))'


def test_select():
    rql = Query().select(['attribute'])
    assert rql.compile() == '?select(attribute)'


def test_like():
    rql = Query().like('product.id', 'PR-')
    assert rql.compile() == '?like(product.id,PR-)'


def test_ilike():
    rql = Query().ilike('product.id', 'PR-')
    assert rql.compile() == '?ilike(product.id,PR-)'


def test_order_by():
    rql = Query().order_by('date')
    assert rql.compile() == '?order_by=date'


def test_greater():
    rql = Query().greater('property', 'value')
    assert rql.compile() == '?gt(property,value)'


def test_greater_equal():
    rql = Query().greater_equal('property', 'value')
    assert rql.compile() == '?ge(property,value)'


def test_lesser():
    rql = Query().lesser('property', 'value')
    assert rql.compile() == '?lt(property,value)'


def test_lesser_equal():
    rql = Query().lesser_equal('property', 'value')
    assert rql.compile() == '?le(property,value)'


def test_limit():
    rql = Query().limit(10)
    assert rql.compile() == '?limit=10'


def test_offset():
    rql = Query().offset(10)
    assert rql.compile() == '?offset=10'


def test_ordering():
    rql = Query().ordering(['property1', 'property2'])
    assert rql.compile() == '?ordering(property1,property2)'
