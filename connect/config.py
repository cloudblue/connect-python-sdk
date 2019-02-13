# -*- coding: utf-8 -*-

import json
import os


class Config(object):
    api_url = None
    api_key = None
    products = []

    def __init__(
            self,
            api_url=None,
            api_key=None,
            products=None,
            file=None,
            **kwargs
    ):
        """
        initialization config for public api
        :param api_url: Public api url
        :param api_key: Service user ApiKey
        :param products (optional): Id products
        :param file: Config file path
        :param kwargs:
        """
        if not all([Config.api_key, Config.api_url]):
            self.load(api_url, api_key, products, file, **kwargs)

    def load(self, api_url, api_key, products, file, **kwargs):
        if not any([api_key, api_url, file]):
            return

        if file:
            return self.load_from_file(file)

        self.check_credentials(api_url, api_key, products)
        self._set_attr(api_url, api_key, products)

    @staticmethod
    def _set_attr(api_url, api_key, products=None):
        Config.api_key = api_key

        # URL must end with a character
        Config.api_url = api_url
        if products:
            Config.products = [products] if isinstance(
                products, str) else products

    @staticmethod
    def check_credentials(api_url, api_key, products):
        """
        :param api_url:
        :param api_key:
        :param products:
        :return: True or raise ValueError
        """
        if not all([api_key, api_url]):
            raise ValueError('Please provide your credentials.'
                             'Not set value for `api_key` or `api_url`')

        if products and not isinstance(products, (str, list)):
            raise TypeError('Products can be string or string list')

        return

    def load_from_file(self, file):
        """
        Format file (json): {
            "api_key":
            "api_url":
            "products" (optional):
        }
        :param file (str): Path to the file
        :return: Init configuration parameters.
                Set Config.api_url/.api_key/.products
        """
        if not os.path.exists(file):
            raise IOError('Not file `{}` on directory'.format(file))

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

        products = products.encode('utf-8') if not isinstance(products, (str, list)) else products
        api_url = api_url.encode('utf-8') if not isinstance(api_url, str) else api_url
        api_key = api_key.encode('utf-8') if not isinstance(api_key, str) else api_key

        self.check_credentials(api_url, api_key, products)
        self._set_attr(api_url, api_key, products)
