# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json
import os


class Config(object):
    # Global instance
    instance = None  # type: Config

    def __init__(
            self,
            api_url=None,
            api_key=None,
            products=None,
            filename=None
    ):
        """
        initialization config for public api
        :param api_url: Public api url
        :param api_key: Service user ApiKey
        :param products (optional): Id products
        :param filename: Config file path
        """
        # Check arguments
        if not filename and not any([api_key, api_url]):
            raise ValueError('Filename or api_key and api_url are expected'
                             'in Config initialization')
        if products and not isinstance(products, (str, list)):
            raise TypeError('Products can be string or string list. Found type '
                            + type(products).__name__)

        # Load config from filename name
        if filename:
            if not os.path.exists(filename):
                raise IOError('Not filename `{}` on directory'.format(filename))

            with open(filename) as config_file:
                configs = config_file.read()

            try:
                configs = json.loads(configs)
            except Exception as ex:
                raise TypeError('Invalid config filename `{}`\n'
                                'ERROR: {}'.format(filename, str(ex)))

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
        if not Config.instance:
            Config.instance = self

    @property
    def api_url(self):
        return self._api_url

    @property
    def api_key(self):
        return self._api_key

    @property
    def products(self):
        return self._products
