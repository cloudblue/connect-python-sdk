# -*- coding: utf-8 -*-

import json
from connect.config import Config
import os

conf_dict = {
    'apiEndpoint': 'http://localhost:8080/api/public/v1/',
    'apiKey': 'ApiKey XXXX:YYYYY',
    'products': 'CN-631-322-000'
}
file_name = 'test_config.json'


def _assert_config():
    assert Config.api_key == conf_dict.get('apiKey')
    assert Config.api_url == conf_dict.get('apiEndpoint')
    assert Config.products == [conf_dict.get('products')]


def _reset_config():
    Config.api_url, Config.api_key, Config.products = None, None, None


def test_init_config_from_json_file():
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path, 'w') as output:
        output.write(json.dumps(conf_dict))

    Config(file=file_path)
    os.remove(file_path)

    _assert_config()
    _reset_config()


def test_set_config():
    Config(
        api_key=conf_dict.get('apiKey'),
        api_url=conf_dict.get('apiEndpoint'),
        products=conf_dict.get('products'),
    )
    _assert_config()
    _reset_config()
