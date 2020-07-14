# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import json
import os


class Config(object):
    """ Initialization config for public api.

    :param str api_url: Public api url.
    :param str api_key: Service user ApiKey.
    :param str|list[str] products: Optional product ids.
    :param str file: Config file name.
    :raises ValueError: Raised if either ``file`` or one of ``api_url`` or ``api_key`` are missing.
    :raises TypeError: Raised if ``products`` is not a string or list of strings, or if config file
        does not contain JSON data.
    :raises IOError: Raised if the specified ``file`` could not be opened.
    """

    # Global instance
    _instance = None  # type: Config

    # noinspection PyShadowingBuiltins
    def __init__(self, api_url=None, api_key=None, products=None, file=None):
        # Check arguments
        if not file and not any([api_key, api_url]):
            raise ValueError('Expected file or api_key and api_url in Config initialization')
        if products and not isinstance(products, (str, list)):
            raise TypeError('Products can be string or string list. Found type '
                            + type(products).__name__)

        # Load config from file name
        if file:
            if not os.path.exists(file):
                raise IOError('No file `{}` on directory `{}`'.format(file, os.getcwd()))

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
        self._api_url = api_url if api_url.endswith('/') else api_url + '/'
        self._products = [products] \
            if isinstance(products, str) and products \
            else products or []

        # Store first created instance
        if not Config._instance:
            Config._instance = self

    @classmethod
    def get_instance(cls):
        """
        :return: Global instance.
        :rtype: :py:class:`.Config`
        """
        if not cls._instance:
            cls._instance = Config(file='config.json')
        return cls._instance

    @property
    def api_url(self):
        """
        :return: Api URL.
        :rtype: str
        """
        return self._api_url

    @property
    def api_key(self):
        """
        :return: ApiKey.
        :rtype: str
        """
        return self._api_key

    @property
    def products(self):
        """
        :return: Valid product ids.
        :rtype: list[str]
        """
        return self._products

    def __str__(self):
        return '<Configuration {}>'.format(
            self.api_url
        )
