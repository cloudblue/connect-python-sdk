# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json

from typing import Any, List, Dict

from connect.logger import function_log
from connect.models import Param, ActivationTileResponse
from connect.models.base import BaseModel
from .base import BaseResource
from .template import TemplateResource


class AutomationResource(BaseResource):
    limit = 1000

    def build_filter(self, status='pending'):
        # type: (str) -> Dict[str, Any]
        filters = super(AutomationResource, self).build_filter()
        if status:
            filters['status'] = status
        return filters

    def process(self):
        # type: () -> None
        for request in self.list:
            self.dispatch(request)

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
        return self.api.post(path=pk + '/approve/', data=data if data else {})

    @function_log
    def inquire(self, pk):
        # type: (str) -> str
        return self.api.post(path=pk + '/inquire/', data={})

    @function_log
    def fail(self, pk, reason):
        # type: (str, str) -> str
        return self.api.post(path=pk + '/fail/', data={'reason': reason})

    @function_log
    def render_template(self, pk, template_id):
        # type: (str, str) -> ActivationTileResponse
        return TemplateResource(self.config).render(template_id, pk)

    @function_log
    def update_parameters(self, pk, params):
        # type: (str, List[Param]) -> str
        list_dict = []
        for _ in params:
            list_dict.append(_.__dict__ if isinstance(_, Param) else _)

        return self.api.put(
            path=pk,
            data=json.dumps({'asset': {'params': list_dict}}),
        )
