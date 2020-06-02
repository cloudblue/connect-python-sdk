# -*- coding: utf-8 -*-
# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from mock import patch, MagicMock
import os

import pytest

from connect.exceptions import ServerError
from connect.models.activation_tile_response import ActivationTileResponse
from connect.resources import TemplateResource
from .common import Response, load_str


def _list_template_response():
    return _get_response_from_file('list_template_response.json')


def _get_template_response():
    return _get_response_from_file('get_template_response.json')


def _get_response_from_file(filename):
    return Response(
        ok=True,
        text=load_str(os.path.join(os.path.dirname(__file__), 'data', filename)),
        status_code=200
    )


def _get_array_response(object_response):
    return Response(
        ok=True,
        text='[{}]'.format(object_response.text),
        status_code=200
    )


def _get_bad_response():
    return Response(
        ok=False,
        text='{}',
        status_code=404
    )


@patch('requests.get')
def test_list_templates(get_mock):
    get_mock.return_value = _get_array_response(_list_template_response())
    template = TemplateResource().list('PRD-845-746-468')
    assert isinstance(template, list)
    assert len(template) == 1

    get_mock.assert_called_with(
        url='http://localhost:8080/public/v1/products/PRD-845-746-468/templates/',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        params={'scope': 'asset', 'type': 'fulfillment'},
        timeout=300)


@patch('requests.get', MagicMock(return_value=_get_bad_response()))
def test_list_template_bad():
    with pytest.raises(ServerError):
        TemplateResource().list('PRD-000-000-000')


@patch('requests.get')
def test_get_template(get_mock):
    get_mock.return_value = _get_template_response()
    template = TemplateResource().get('TL-313-655-502')
    assert template.template_id == 'TL-313-655-502'


def test_render_bad():
    template_resource = TemplateResource()
    with pytest.raises(ValueError) as e:
        template_resource.render(None, None)
        assert str(e.value) == 'Invalid ids for render template'


@patch('requests.get')
def test_renders(get_mock):
    get_mock.return_value = Response(
        ok=True,
        text='# Sample Activation Template',
        status_code=200,
    )
    template_resource = TemplateResource()
    response = template_resource.render('TL-313-655-502', 'PR-845-746-468')
    assert isinstance(response, ActivationTileResponse)
    assert response.tile == '# Sample Activation Template'

    get_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/templates/TL-313-655-502/render',
        params={'request_id': 'PR-845-746-468'},
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        timeout=300)
