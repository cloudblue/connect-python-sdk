# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

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


def test_global_implicit_global_config():
    """ Global config is instantiated from config.json if not explicitly set """
    assert Config.get_instance().api_key == conf_dict.get('apiKey')
    assert Config.get_instance().api_url == conf_dict.get('apiEndpoint')
    assert isinstance(Config.get_instance().products, list)
    assert len(Config.get_instance().products) == 1
    assert Config.get_instance().products[0] == conf_dict.get('products')


# noinspection PyPropertyAccess
def test_global_config_immutable_properties():
    with pytest.raises(AttributeError):
        Config.get_instance().api_key = conf_dict.get('apiKey')
        Config.get_instance().api_url = conf_dict.get('apiEndpoint')
        Config.get_instance().products = [conf_dict.get('products')]


def test_init_config_with_non_existing_file():
    with pytest.raises(IOError):
        Config(file='non_existing_config.json')


def test_init_config_with_file():
    _assert_config(Config(file='config.json'))


def test_init_config_with_arguments():
    _assert_config(Config(
        api_key=conf_dict.get('apiKey'),
        api_url=conf_dict.get('apiEndpoint'),
        products=conf_dict.get('products'),
    ))


def test_init_config_with_invalid_arguments():
    with pytest.raises(ValueError):
        Config(
            api_key='',
            api_url='',
            products='',
        )


# noinspection PyPropertyAccess
def test_config_immutable_properties():
    config = Config(file='config.json')
    with pytest.raises(AttributeError):
        config.api_key = conf_dict.get('apiKey')
        config.api_url = conf_dict.get('apiEndpoint')
        config.products = [conf_dict.get('products')]


def _assert_config(config):
    assert config.api_key == conf_dict.get('apiKey')
    assert config.api_url == conf_dict.get('apiEndpoint')
    assert isinstance(config.products, list)
    assert len(config.products) == 1
    assert config.products[0] == conf_dict.get('products')
