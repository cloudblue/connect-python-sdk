# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import functools
from typing import Any, List, Dict, Union

import marshmallow
import requests
from requests import compat

from connect.config import Config
from connect.logger import function_log, logger
from connect.models import BaseSchema, ServerErrorSchema
from connect.models.exception import ServerErrorException


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
        # type: () -> Dict[str, str]
        return {
            'Authorization': (self.config.api_key
                              if self.config.api_key.startswith('ApiKey ')
                              else 'ApiKey ' + self.config.api_key),
            'Content-Type': 'application/json',
        }

    @staticmethod
    def check_response(response):
        # type: (requests.Response) -> str
        if not hasattr(response, 'content'):
            raise AttributeError(
                'Response does not have attribute content. Check your request params. '
                'Response status - {}'.format(response.status_code),
            )

        if not hasattr(response, 'ok') or not response.ok:
            data, error = ServerErrorSchema().loads(response.content)
            if data:
                raise ServerErrorException(data)

        return response.content

    @function_log
    def get(self, url, params=None, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        response = requests.get(url, params, **kwargs)
        return self.check_response(response)

    @function_log
    def post(self, url, data=None, json=None, **kwargs):
        if 'headers' not in kwargs:
            kwargs['headers'] = self.headers
        response = requests.post(url, data, json, **kwargs)
        return self.check_response(response)

    @function_log
    def put(self, url, data=None, **kwargs):
        if 'headers' not in kwargs:
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
        # type: () -> List[Any]
        filters = self.build_filter()
        logger.info('Get list request by filter - {}'.format(filters))
        response = self.api.get(url=self.url, params=filters)
        return self._load_schema(response)

    @property
    def url(self):
        return self.urljoin(self.config.api_url, self.resource)

    def build_filter(self):
        # type: () -> Dict[str, Any]
        res_filter = {}
        if self.limit:
            res_filter['limit'] = self.limit
        return res_filter

    def get(self, pk):
        # type: (str) -> Any
        response = self.api.get(url=self.urljoin(self.url, pk))
        objects = self._load_schema(response)
        if isinstance(objects, list) and len(objects) > 0:
            return objects[0]

    @staticmethod
    def urljoin(*args):
        return functools.reduce(
            lambda a, b: compat.urljoin(a + ('' if a.endswith('/') else '/'), b),
            args)

    def _load_schema(self, response, many=None):
        # type: (str, bool) -> Union[List[Any], Any]
        objects, error = self.schema.loads(response, many)
        if error:
            raise TypeError(
                'Invalid structure for initialization of `{}`. \n'
                'Error: {}. \nServer Response: {}'.format(type(self).__name__, error, response),
            )

        return objects
