# -*- coding: utf-8 -*-

import requests

from connect.config import Config
from connect.logger import function_log, logger
from connect.models import BaseScheme, ServerErrorScheme
from connect.models.exception import ServerErrorException
from .utils import joinurl

config = Config()


class ApiClient(object):

    @property
    def headers(self):
        config.check_credentials(
            config.api_url, config.api_key, config.products)
        return {
            "Authorization": config.api_key,
            "Content-Type": "application/json",
        }

    @staticmethod
    def check_response(response):
        if not hasattr(response, 'content'):
            raise AttributeError(
                'Response not attribute content. Check your request params'
                'Response status - {}'.format(getattr(response, 'code')),
            )

        if not hasattr(response, 'ok') or not response.ok:
            data, error = ServerErrorScheme().loads(response.content)
            if data:
                raise ServerErrorException(data)

        return response.content

    @function_log
    def get(self, url, params=None, **kwargs):
        kwargs['headers'] = self.headers
        response = requests.get(url, params, **kwargs)
        return self.check_response(response)

    @function_log
    def post(self, url, data=None, json=None, **kwargs):
        kwargs['headers'] = self.headers
        response = requests.post(url, data, json, **kwargs)
        return self.check_response(response)

    @function_log
    def put(self, url, data=None, **kwargs):
        kwargs['headers'] = self.headers
        response = requests.put(url, data, **kwargs)
        return self.check_response(response)


class BaseResource(object):
    resource = None
    limit = 100
    api = ApiClient()
    scheme = BaseScheme()

    def __init__(self, *args, **kwargs):

        if self.__class__.resource is None:
            raise AttributeError('Resource name not specified in class {}'.format(
                self.__class__.__name__) + '. Add an attribute `resource` name of the resource')

    def build_filter(self):
        res_filter = {}
        if self.limit:
            res_filter['limit'] = self.limit

        return res_filter

    @property
    def _list_url(self):
        return joinurl(config.api_url, self.__class__.resource)

    def _obj_url(self, pk):
        return joinurl(self._list_url, pk)

    def __loads_scheme(self, response):
        objects, error = self.scheme.loads(response, many=True)
        if error:
            raise TypeError(
                'Invalid structure for initialisation objects. \n'
                'Error: {}. \nServer Response: {}'.format(error, response),
            )

        return objects

    def get(self, pk):
        response = self.api.get(url=self._obj_url(pk))
        objects = self.__loads_scheme(response)
        if isinstance(objects, list) and len(objects) > 0:
            return objects[0]

    def list(self):
        filters = self.build_filter()
        logger.info('Get list request by filter - {}'.format(filters))
        response = self.api.get(url=self._list_url, params=filters)
        return self.__loads_scheme(response)
