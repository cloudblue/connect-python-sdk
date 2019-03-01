# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import os

import pytest

from connect.config import Config


conf_dict = {
    'apiEndpoint': 'http://localhost:8080/api/public/v1/',
    'apiKey': 'ApiKey XXXX:YYYYY',
    'products': 'CN-631-322-000'
}


def setup_module(module):
    module.prev_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def teardown_module(module):
    os.chdir(module.prev_dir)


def teardown_function():
    Config.api_url, Config.api_key, Config.products = None, None, None


def test_init_config_with_non_existing_file():
    with pytest.raises(IOError):
        Config(file='non_existing_config.json')


def test_init_config_with_file():
    config = Config(file='config.json')
    _assert_config(config)


def test_set_config():
    config = Config(
        api_key=conf_dict.get('apiKey'),
        api_url=conf_dict.get('apiEndpoint'),
        products=conf_dict.get('products'),
    )
    _assert_config(config)


def _assert_config(config=None):
    assert Config.api_key == conf_dict.get('apiKey')
    assert Config.api_url == conf_dict.get('apiEndpoint')
    assert isinstance(Config.products, list)
    assert len(Config.products) == 1
    assert Config.products == [conf_dict.get('products')]
    if config:
        assert config.api_key == conf_dict.get('apiKey')
        assert config.api_url == conf_dict.get('apiEndpoint')
        assert isinstance(config.products, list)
        assert len(config.products) == 1
        assert config.products == [conf_dict.get('products')]
