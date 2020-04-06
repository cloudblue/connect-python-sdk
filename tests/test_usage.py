# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
import time
from datetime import date, timedelta

import pytest
from mock import patch, MagicMock, call

from connect.exceptions import FileRetrievalError
from connect.models import Contract, Product, UsageRecord, UsageFile
from connect.resources import UsageAutomation
from .common import Response, load_str, BinaryResponse


def _get_response_ok():
    return Response(
        ok=True,
        text=load_str(os.path.join(os.path.dirname(__file__), 'data', 'response_usage.json')),
        status_code=200)


def _get_response_ok2():
    return Response(
        ok=True,
        text=load_str(os.path.join(os.path.dirname(__file__), 'data', 'response_usage2.json')),
        status_code=201)


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
def test_create_resource():
    requests = UsageAutomation().list()
    assert isinstance(requests, list)
    assert len(requests) == 8


@patch('requests.get', MagicMock(return_value=_get_response_ok()))
@patch('requests.post', MagicMock(return_value=_get_response_ok2()))
def test_process():
    resource = UsageAutomationTester()
    resource.process()


@patch('requests.get')
def test_get_usage_template_ok(get_mock):
    get_mock.side_effect = [
        Response(ok=True, text='{"template_link": "..."}', status_code=200),
        BinaryResponse(ok=True, content=b'template_contents', status_code=200)]
    resource = UsageAutomation()
    assert resource.get_usage_template(Product(id='PRD-638-321-603')) == b'template_contents'
    get_mock.assert_has_calls([
        call(
            url='http://localhost:8080/api/public/v1/usage/products/PRD-638-321-603/template/',
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300),
        call('...')
    ])


@patch('requests.get', MagicMock(return_value=Response(
    ok=True, text='{}', status_code=200)))
def test_get_usage_template_no_link():
    resource = UsageAutomation()
    with pytest.raises(FileRetrievalError):
        resource.get_usage_template(Product(id='PRD-638-321-603'))


@patch('requests.get', MagicMock(side_effect=[
    Response(ok=True, text='{"template_link": "..."}', status_code=200),
    BinaryResponse(ok=True, content=None, status_code=200)]))
def test_get_usage_template_no_file():
    resource = UsageAutomation()
    with pytest.raises(FileRetrievalError):
        resource.get_usage_template(Product(id='PRD-638-321-603'))


class UsageAutomationTester(UsageAutomation):
    def process_request(self, request):
        # type: (UsageFile) -> None
        if request.contract.id == 'CRD-99082-45842-69181':
            usage_file = UsageFile(
                name='sdk test',
                product=Product(id=request.product.id),
                contract=Contract(id=request.contract.id)
            )
            usages = [UsageRecord(
                item_search_criteria='item.mpn',
                item_search_value='SKUA',
                quantity=1,
                start_time_utc=(date.today() - timedelta(1)).strftime('%Y-%m-%d'),
                end_time_utc=time.strftime('%Y-%m-%d %H:%M:%S'),
                asset_search_criteria='parameter.param_b',
                asset_search_value='tenant2'
            )]
            self.submit_usage(usage_file, usages)
        elif request.contract.id == 'CRD-99082-45842-69182':
            pass
        elif request.contract.id == 'CRD-99082-45842-69183':
            pass
        elif request.contract.id == 'CRD-99082-45842-69184':
            usage_file = UsageFile(
                product=Product(id=request.product.id),
                contract=Contract(id=request.contract.id)
            )
            usages = [UsageRecord(
                record_id='123',
                item_search_criteria='item.mpn',
                item_search_value='SKUA',
                quantity=1,
                start_time_utc=(date.today() - timedelta(1)).strftime('%Y-%m-%d'),
                end_time_utc=time.strftime('%Y-%m-%d %H:%M:%S'),
                asset_search_criteria='parameter.param_b',
                asset_search_value='tenant2'
            )]
            self.submit_usage(usage_file, usages)
        elif request.contract.id == 'CRD-99082-45842-69185':
            pass
        elif request.contract.id == 'CRD-99082-45842-69186':
            pass
        elif request.contract.id == 'CRD-99082-45842-69187':
            pass
        else:
            raise UserWarning('Invalid test')
