# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import functools
from typing import Any, List, Dict, Tuple

import requests
from requests import compat

from connect.config import Config
from connect.exceptions import ServerError
from connect.logger import function_log, logger
from connect.models import BaseModel, ServerErrorResponse


class ApiClient(object):
    def __init__(self, config, base_path):
        # type: (Config, str) -> None

        # Set base URL
        self._base_path = base_path

        # Set passed config or globally configured instance
        self._config = config or Config.get_instance()
        if not isinstance(self._config, Config):
            raise ValueError('A valid Config object must be passed or globally configured.')

    @property
    def base_path(self):
        # type: () -> str
        return self._base_path

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

    def get_url(self, path=''):
        # type: (str) -> str
        return self.urljoin(self.config.api_url, self.base_path, path)

    @staticmethod
    def urljoin(*args):
        # type: (str) -> str
        return functools.reduce(
            lambda a, b: compat.urljoin(a + ('' if a.endswith('/') else '/'), b),
            args)

    @function_log
    def get(self, path='', **kwargs):
        # type: (str, Any) -> Tuple[str, int]
        kwargs = self._fix_request_kwargs(path, kwargs)
        response = requests.get(**kwargs)
        return self._check_and_pack_response(response)

    @function_log
    def post(self, path='', **kwargs):
        # type: (str, Any) -> Tuple[str, int]
        kwargs = self._fix_request_kwargs(path, kwargs)
        response = requests.post(**kwargs)
        return self._check_and_pack_response(response)

    @function_log
    def put(self, path='', **kwargs):
        # type: (str, Any) -> Tuple[str, int]
        kwargs = self._fix_request_kwargs(path, kwargs)
        response = requests.put(**kwargs)
        return self._check_and_pack_response(response)

    def _fix_request_kwargs(self, path, prev_kwargs, **kwargs):
        # type: (str, Dict[str, Any], Dict[str, Any]) -> Dict[str, Any]
        """ Set correct kwargs for requests """
        fixed_kwargs = prev_kwargs.copy()
        fixed_kwargs.update(kwargs)
        if 'url' not in fixed_kwargs:
            fixed_kwargs['url'] = self.get_url(path)
        if 'headers' not in fixed_kwargs:
            fixed_kwargs['headers'] = self.headers
        return fixed_kwargs

    @staticmethod
    def _check_and_pack_response(response):
        # type: (requests.Response) -> Tuple[str, int]
        request_attrs = ('text', 'status_code', 'ok')
        for attr in request_attrs:
            if not hasattr(response, attr):
                raise AttributeError(
                    'Response does not have attribute `{}`. Check your request params. '
                    'Response status - {}'.format(attr, response.status_code),
                )

        if not response.ok:
            error = ServerErrorResponse.deserialize(response.text)
            raise ServerError(error)

        return response.text, response.status_code


class BaseResource(object):
    """ Base class of all resources.

    :param Config config: Config object or ``None`` to use environment config (default).
    """

    resource = None  # type: str
    limit = 100  # type: int
    model_class = BaseModel

    def __init__(self, config=None):
        # Set client
        if not self.__class__.resource:
            raise AttributeError('Resource name not specified in class {}. '
                                 'Add an attribute `resource` with the name of the resource'
                                 .format(self.__class__.__name__))
        self._api = ApiClient(config, self.__class__.resource)

    @property
    def config(self):
        # type: () -> Config
        return self._api.config

    def get(self, pk):
        # type: (str) -> Any
        response, _ = self._api.get(path=pk)
        objects = self.model_class.deserialize(response)
        if isinstance(objects, list) and len(objects) > 0:
            return objects[0]

    def filters(self, **kwargs):
        # type: (Dict[str, Any]) -> Dict[str, Any]
        filters = {}
        if self.limit:
            filters['limit'] = self.limit
        for key, val in kwargs.items():
            filters[key] = val
        return filters

    def list(self, filters=None):
        # type: (Dict[str, Any]) -> List[Any]
        filters = filters or self.filters()
        logger.info('Get list request with filters - {}'.format(filters))
        response, _ = self._api.get(params=filters)
        return self.model_class.deserialize(response)
