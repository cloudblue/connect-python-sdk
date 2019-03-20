# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import marshmallow
import requests
from functools import reduce
from typing import Any

from connect.config import Config
from connect.logger import function_log, logger
from connect.models import BaseSchema, ServerErrorSchema
from connect.models.exception import ServerErrorException
from .utils import join_url


class ApiClient(object):
    def __init__(self, config=None):
        # type: (Config) -> None

        # Assign passed config or globally configured instance
        self._config = config or Config.get_instance()

        # Assert data
        if not isinstance(self.config, Config):
            raise ValueError('A valid Config object is required to create an ApiClient')

    @property
    def config(self):
        # type: () -> Config
        return self._config

    @property
    def headers(self):
        # type: () -> dict
        return {
            "Authorization": self.config.api_key,
            "Content-Type": "application/json",
        }

    @staticmethod
    def check_response(response):
        # type: (requests.Response) -> str
        if not hasattr(response, 'content'):
            raise AttributeError(
                'Response not attribute content. Check your request params'
                'Response status - {}'.format(getattr(response, 'code')),
            )

        if not hasattr(response, 'ok') or not response.ok:
            data, error = ServerErrorSchema().loads(response.content)
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
    resource = None  # type: str
    limit = 100  # type: int
    api = None  # type: ApiClient
    schema = BaseSchema()  # type: marshmallow.Schema

    def __init__(self, config=None):
        # Assign passed config or globally configured instance
        self._config = config or Config.get_instance()

        # Assert data
        if not self.__class__.resource:
            raise AttributeError('Resource name not specified in class {}'.format(
                self.__class__.__name__) + '. Add an attribute `resource` name of the resource')
        if not isinstance(self.config, Config):
            raise ValueError('A valid Config object must be passed or globally configured '
                             'to create a ' + type(self).__name__)
        if not BaseResource.api:
            BaseResource.api = ApiClient(config)

    @property
    def config(self):
        # type: () -> Config
        return self._config

    @property
    def list(self):
        # type: () -> Any
        filters = self.build_filter()
        logger.info('Get list request by filter - {}'.format(filters))
        response = self.api.get(url=self._list_url, params=filters)
        return self._load_schema(response)

    def build_filter(self):
        # type: () -> dict
        res_filter = {}
        if self.limit:
            res_filter['limit'] = self.limit
        return res_filter

    def get(self, pk):
        # type: (str) -> Any
        response = self.api.get(url=self._obj_url(pk))
        objects = self._load_schema(response)
        if isinstance(objects, list) and len(objects) > 0:
            return objects[0]

    @property
    def _list_url(self):
        # type: () -> str
        return join_url(self.config.api_url, self.__class__.resource)

    def _obj_url(self, *args):
        # type: ([str]) -> str
        return reduce(lambda x, y: join_url(x, y), args, self._list_url)

    def _load_schema(self, response):
        # type: (str) -> Any
        objects, error = self.schema.loads(response, many=True)
        if error:
            raise TypeError(
                'Invalid structure for initialization of `{}`. \n'
                'Error: {}. \nServer Response: {}'.format(type(self).__name__, error, response),
            )

        return objects
