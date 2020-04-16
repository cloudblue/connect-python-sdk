# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import copy
import logging
from typing import Any, Dict

from connect.logger import function_log, logger as global_logger
from connect.models.activation_tile_response import ActivationTileResponse
from connect.models.base import BaseModel
from .base import BaseResource
from .template import TemplateResource


class AutomationEngine(BaseResource):
    limit = 1000  # type: int
    logger = logging.getLogger()

    def filters(self, status='pending', **kwargs):
        # type: (str, Dict[str, Any]) -> Dict[str, Any]
        return super(AutomationEngine, self).filters(status=status, **kwargs)

    @function_log(custom_logger=logger)
    def process(self, filters=None):
        '''
        # type: (Dict[str, Any]) -> None
        '''
        for request in self.list(filters):
            self.dispatch(request)

    def dispatch(self, request):
        # type: (BaseModel) -> str
        raise NotImplementedError('Please implement `{}.dispatch` method'
                                  .format(self.__class__.__name__))

    def process_request(self, request):
        raise NotImplementedError('Please implement `{}.process_request` method'
                                  .format(self.__class__.__name__))

    @function_log(custom_logger=logger)
    def approve(self, pk, data):
        # type: (str, dict) -> str
        return self._api.post(path=pk + '/approve/', json=data)[0]

    @function_log(custom_logger=logger)
    def inquire(self, pk):
        # type: (str) -> str
        return self._api.post(path=pk + '/inquire/', json={})[0]

    @function_log(custom_logger=logger)
    def fail(self, pk, reason):
        # type: (str, str) -> str
        return self._api.post(path=pk + '/fail/', json={'reason': reason})[0]

    @function_log(custom_logger=logger)
    def render_template(self, pk, template_id):
        # type: (str, str) -> ActivationTileResponse
        return TemplateResource(self.config).render(template_id, pk)

    def _set_custom_logger(self, *args):
        handlers = [copy.copy(hdlr) for hdlr in global_logger.handlers]
        log_level = global_logger.level
        self.__class__.logger.setLevel(log_level)
        self.__class__.logger.propagate = False
        self.__class__.logger.handlers = handlers
        base = " %(levelname)-6s; %(asctime)s; %(name)-6s; %(module)s:%(funcName)s:line" \
               "-%(lineno)d: %(message)s"
        sformat = " ".join(args) + base
        [handler.setFormatter(logging.Formatter(sformat))
         for handler in self.__class__.logger.handlers]
