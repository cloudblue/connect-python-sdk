# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from collections import namedtuple

import pytest
import requests
from mock import patch, MagicMock

from connect.models.exception import FileRetrievalError
from connect.models.product import Product
from connect.resource import UsageAutomation

Response = namedtuple('Response', ('ok', 'content', 'text'))


@patch('requests.get',
       MagicMock(return_value=Response(ok=True, content='{"template_link": "..."}', text='test')))
def test_get_usage_template_ok():
    assert UsageAutomation().get_usage_template(Product(id='PRD-638-321-603')) == 'test'


@patch('requests.get', MagicMock(return_value=Response(ok=True, content='{}', text='')))
def test_get_usage_template_no_link():
    with pytest.raises(FileRetrievalError):
        UsageAutomation().get_usage_template(Product(id='PRD-638-321-603'))


@patch('requests.get', MagicMock(return_value=Response(ok=True, content='{"template_link": "..."}', text=None)))
def test_get_usage_template_no_file():
    with pytest.raises(FileRetrievalError):
        UsageAutomation().get_usage_template(Product(id='PRD-638-321-603'))
