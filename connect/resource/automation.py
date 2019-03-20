# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json

from typing import Any

from connect.logger import function_log
from connect.models import Param, ActivationTileResponse
from connect.models.base import BaseModel
from .base import BaseResource
from .template import TemplateResource
from .utils import join_url


class AutomationResource(BaseResource):
    limit = 1000

    def build_filter(self):
        # type: () -> dict
        filters = super(AutomationResource, self).build_filter()
        filters['status'] = 'pending'
        return filters

    def process(self):
        # type: () -> Any
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
        url = join_url(self._obj_url(pk), 'approve/')
        return self.api.post(url=url, data=data if data else {})

    @function_log
    def inquire(self, pk):
        # type: (str) -> str
        url = join_url(self._obj_url(pk), 'inquire/')
        return self.api.post(url=url, data={})

    @function_log
    def fail(self, pk, reason):
        # type: (str, str) -> str
        url = join_url(self._obj_url(pk), 'fail/')
        return self.api.post(url=url, data={'reason': reason})

    @function_log
    def render_template(self, pk, template_id):
        # type: (str, str) -> ActivationTileResponse
        return TemplateResource(self.config).render(template_id, pk)

    @function_log
    def update_parameters(self, pk, params):
        # type: (str, list) -> str
        list_dict = []
        for _ in params:
            list_dict.append(_.__dict__ if isinstance(_, Param) else _)

        return self.api.put(
            url=self._obj_url(pk),
            data=json.dumps({'asset': {'params': list_dict}}),
        )
