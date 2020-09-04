# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os
import unittest
import pytest

from mock import Mock, call, patch

from connect.config import Config
from connect.models import Item
from connect.resources.product import ProductsResource

from .common import Response, load_json, load_str

get_parameters_contents = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_get_parameters.json'))
create_parameter_body = load_json(
    os.path.join(os.path.dirname(__file__), 'data', 'create_parameter_request.json'))
create_parameter_response = load_json(
    os.path.join(os.path.dirname(__file__), 'data', 'response_create_parameter.json'))


class TestParameters(unittest.TestCase):

    def setUp(self):
        self.config = Config(file='tests/config.json')

    @patch('requests.get')
    def test_parameters_request_ok(self, get_mock):
        # type: (Mock) -> None
        get_mock.side_effect = [
            Response(True, '[' + get_parameters_contents + ']', 200),
            Response(True, get_parameters_contents, 200)
        ]

        request = ProductsResource(config=self.config)
        result = request.list_parameters('PRD-075-401-854')
        assert get_mock.call_count == 1
        self.assertEqual(len(result), 1, msg=None)

        get_mock.assert_has_calls([
            call(
                headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
                timeout=300,
                url=('http://localhost:8080/public/v1/'
                     'products/PRD-075-401-854/parameters/'))
        ])

    @patch('requests.get')
    def test_parameter_empty(self, get_mock):
        # type: (Mock) -> None
        get_mock.return_value = Response(True, '[]', 200)

        request = ProductsResource(config=self.config)
        result = request.list_parameters('PRD-000-000-000')
        assert get_mock.call_count == 1
        url = 'http://localhost:8080/public/v1/products/PRD-000-000-000/parameters/'
        get_mock.assert_has_calls([
            call(
                headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
                timeout=300,
                url=url
                )
        ])
        self.assertEqual(result, [], msg=None)

    @patch('requests.post')
    def test_create_parameter(self, post_mock):
        # type: (Mock) -> None
        post_mock.return_value = Response(True, create_parameter_response, 200)
        body = create_parameter_body
        request = ProductsResource(config=self.config)
        request.create_parameter('PRD-075-401-854', body)

        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json=body,
            timeout=300,
            url='http://localhost:8080/public/v1/products/PRD-075-401-854/parameters/')

    def test_create_parameter_bad(self):
        request = ProductsResource(config=self.config)
        with pytest.raises(ValueError) as e:
            request.create_parameter(None, None)
        assert str(e.value) == 'Invalid ID'

    @patch('requests.put')
    def test_modify_parameter(self, put_mock):
        modify_parameter_response = create_parameter_response
        put_mock.return_value = Response(True, modify_parameter_response, 200)
        body = modify_parameter_response
        request = ProductsResource(config=self.config)
        request.update_parameter('PRD-075-401-854', 'PRM-075-401-854-0004', body)
        url = ('http://localhost:8080/public/v1'
               '/products/PRD-075-401-854/parameters/PRM-075-401-854-0004')
        put_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json=body,
            timeout=300,
            url=url)

    def test_modify_parameter_bad(self):
        request = ProductsResource(config=self.config)
        with pytest.raises(ValueError) as e:
            request.update_parameter(None, None, None)
        assert str(e.value) == 'Invalid ID'

    @patch('requests.delete')
    def test_delete_parameter(self, delete_mock):
        delete_mock.return_value = Response(True, '[]', 204)
        request = ProductsResource(config=self.config)
        request.delete_parameter('PRD-075-401-854', 'PRM-075-401-854-0004')
        url = ('http://localhost:8080/public/v1'
               '/products/PRD-075-401-854/parameters/PRM-075-401-854-0004')
        delete_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url=url)

    def test_delete_parameter_bad(self):
        request = ProductsResource(config=self.config)
        with pytest.raises(ValueError) as e:
            request.delete_parameter(None, None)
        assert str(e.value) == 'Invalid ID'


class TestItems(unittest.TestCase):

    def setUp(self):
        self.config = Config(file='tests/config.json')

    def test_items(self):
        product_resource = ProductsResource(config=self.config)
        item_resource = product_resource.items('PRD-000')
        assert item_resource.resource == 'products/PRD-000/items'
        assert item_resource.model_class == Item

        item_resource = product_resource.items('PRD-001')
        assert item_resource.resource == 'products/PRD-001/items'


if __name__ == "__main__":
    unittest.main()
