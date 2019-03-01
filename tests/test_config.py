import os

import pytest

from connectsdk.config import Config


def setup_module(module):
    module.prev_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


def teardown_module(module):
    os.chdir(module.prev_dir)


def test_create_with_non_existing_file():
    with pytest.raises(IOError):
        Config(file='non_existing_config.json')


def test_create_with_file():
    config = Config(file='config.json')
    assert config.api_url == 'http://localhost:8080/api/public/v1/'
    assert config.api_key == 'ApiKey XXXX:YYYYY'
    assert isinstance(config.products, list)
    assert len(config.products) == 1
    assert config.products[0] == 'CN-631-322-000'
