# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json
import os

from typing import List, Union


class Config(object):
    # Global instance
    _instance = None  # type: Config

    # noinspection PyShadowingBuiltins
    def __init__(
            self,
            api_url=None,  # type: str
            api_key=None,  # type: str
            products=None,  # type: Union[str, List[str]]
            file=None  # type: str
    ):
        """
        Initialization config for public api
        :param api_url: Public api url
        :param api_key: Service user ApiKey
        :param products (optional): Id products
        :param file: Config file name
        """

        # Check arguments
        if not file and not any([api_key, api_url]):
            raise ValueError('Filename or api_key and api_url are expected'
                             'in Config initialization')
        if products and not isinstance(products, (str, list)):
            raise TypeError('Products can be string or string list. Found type '
                            + type(products).__name__)

        # Load config from file name
        if file:
            if not os.path.exists(file):
                raise IOError('No file `{}` on directory'.format(file))

            with open(file) as config_file:
                configs = config_file.read()

            try:
                configs = json.loads(configs)
            except Exception as ex:
                raise TypeError('Invalid config file `{}`\n'
                                'ERROR: {}'.format(file, str(ex)))

            (api_url, api_key, products) = (configs.get('apiEndpoint', ''),
                                            configs.get('apiKey', ''),
                                            configs.get('products', ''))
            api_url = api_url.encode('utf-8') if not isinstance(api_url, str) else api_url
            api_key = api_key.encode('utf-8') if not isinstance(api_key, str) else api_key
            products = products.encode('utf-8') \
                if not isinstance(products, (str, list)) \
                else products

        # Initialize
        self._api_key = api_key
        self._api_url = api_url
        self._products = [products] \
            if isinstance(products, str) \
            else products or []

        # Store first created instance
        if not Config._instance:
            Config._instance = self

    @classmethod
    def get_instance(cls):
        # type: () -> Config
        if not cls._instance:
            cls._instance = Config(file='config.json')
        return cls._instance

    @property
    def api_url(self):
        # type: () -> str
        return self._api_url

    @property
    def api_key(self):
        # type: () -> str
        return self._api_key

    @property
    def products(self):
        # type: () -> List[str]
        return self._products
