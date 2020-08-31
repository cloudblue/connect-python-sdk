# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import logging
from typing import Any, Dict, Optional

from connect.logger import function_log, LoggerAdapter
from connect.models.activation_tile_response import ActivationTileResponse
from connect.models.base import BaseModel
from .base import BaseResource
from .template import TemplateResource


class AutomationEngine(BaseResource):
    limit = 1000  # type: int

    def __init__(self, config=None):
        super(AutomationEngine, self).__init__(config)
        self._current_request = None
        self._logger_adapter = None

    def filters(self, status='pending', **kwargs):
        # type: (str, Dict[str, Any]) -> Dict[str, Any]
        return super(AutomationEngine, self).filters(status=status, **kwargs)

    @function_log
    def process(self, filters=None):
        # # type: (Dict[str, Any]) -> None
        for request in self.list(filters):
            self._set_current_request(request)
            self.dispatch(request)
            self._set_current_request(None)

    def dispatch(self, request):
        # type: (BaseModel) -> str
        raise NotImplementedError('Please implement `{}.dispatch` method'
                                  .format(self.__class__.__name__))

    def process_request(self, request):
        raise NotImplementedError('Please implement `{}.process_request` method'
                                  .format(self.__class__.__name__))

    @function_log
    def approve(self, pk, data):
        # type: (str, dict) -> str
        return self._api.post(path=pk + '/approve/', json=data)[0]

    @function_log
    def inquire(self, pk):
        # type: (str) -> str
        return self._api.post(path=pk + '/inquire/', json={})[0]

    @function_log
    def fail(self, pk, reason):
        # type: (str, str) -> str
        return self._api.post(path=pk + '/fail/', json={'reason': reason})[0]

    @function_log
    def render_template(self, pk, template_id):
        # type: (str, str) -> ActivationTileResponse
        return TemplateResource(self.config).render(template_id, pk)

    @property
    def logger(self):
        # type: () -> logging.LoggerAdapter
        request_id = self._current_request.id if self._current_request else 'global'
        name = self.__class__.__name__ + '.' + request_id
        if not self._logger_adapter or self._logger_adapter.logger.name != name:
            self._logger_adapter = LoggerAdapter(logging.getLogger(name))
        return self._logger_adapter

    def _set_current_request(self, request):
        # type: (Optional[BaseModel]) -> None
        self._current_request = request
        self._set_logger_prefix(request)

    def _set_logger_prefix(self, request):
        # type: (Optional[BaseModel]) -> None
        pass
