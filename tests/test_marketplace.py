# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from mock import MagicMock, patch

import pytest
from requests import RequestException

from .common import Response
from connect.exceptions import DeleteResourceError, ServerError, UpdateResourceError
from connect.models import ServerErrorResponse
from connect.resources import MarketplaceResource


ICON_FILE = 'tests/data/icon.png'


@patch('requests.post')
def test_set_icon_ok(post_mock):
    post_mock.return_value = Response(True, None, 200)
    with open(ICON_FILE, 'rb') as f:
        icon = f.read()

    MarketplaceResource().set_icon('MP-XXX', ICON_FILE)

    post_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/marketplaces/MP-XXX/icon',
        headers={'Accept': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        files={'icon': (ICON_FILE, icon)},
        timeout=300)


def test_set_icon_bad_file():
    with pytest.raises(UpdateResourceError):
        MarketplaceResource().set_icon('MP-XXX', 'non_existing_icon.png')


@patch('requests.post', MagicMock(side_effect=RequestException()))
def test_set_icon_request_exception():
    with pytest.raises(UpdateResourceError):
        MarketplaceResource().set_icon('MP-XXX', ICON_FILE)


@patch('requests.post', MagicMock(side_effect=ServerError(ServerErrorResponse())))
def test_set_icon_server_error():
    with pytest.raises(UpdateResourceError):
        MarketplaceResource().set_icon('MP-XXX', ICON_FILE)


@patch('requests.post', MagicMock(return_value=Response(False, '', 500)))
def test_set_icon_status_500():
    with pytest.raises(UpdateResourceError):
        MarketplaceResource().set_icon('MP-XXX', ICON_FILE)


@patch('requests.delete')
def test_delete_ok(delete_mock):
    delete_mock.return_value = Response(True, None, 204)

    MarketplaceResource().delete('MP-XXX')

    delete_mock.assert_called_with(
        url='http://localhost:8080/api/public/v1/marketplaces/MP-XXX',
        headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
        timeout=300)


@patch('requests.delete', MagicMock(side_effect=RequestException()))
def test_delete_request_exception():
    with pytest.raises(DeleteResourceError):
        MarketplaceResource().delete('MP-XXX')


@patch('requests.delete', MagicMock(side_effect=ServerError(ServerErrorResponse())))
def test_delete_server_error():
    with pytest.raises(DeleteResourceError):
        MarketplaceResource().delete('MP-XXX')


@patch('requests.delete', MagicMock(return_value=Response(False, '', 500)))
def test_delete_status_500():
    with pytest.raises(DeleteResourceError):
        MarketplaceResource().delete('MP-XXX')
