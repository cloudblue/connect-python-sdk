# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json

from typing import List

from connect.logger import function_log
from connect.models import FulfillmentSchema, Param, ActivationTileResponse
from .base import BaseResource
from .template import TemplateResource
from .utils import join_url


class FulfillmentResource(BaseResource):
    resource = 'requests'
    limit = 1000
    schema = FulfillmentSchema()

    def build_filter(self):
        # type: () -> dict
        filters = super(FulfillmentResource, self).build_filter()
        if self.config.products:
            filters['asset.product.id__in'] = ','.join(self.config.products)

        filters['status'] = 'pending'
        return filters

    @function_log
    def approve(self, pk, data):
        # type: (str, dict) -> str
        url = join_url(self._obj_url(pk), 'approve/')
        return self.api.post(url=url, data=json.dumps(data if data else {}))

    @function_log
    def inquire(self, pk):
        # type: (str) -> str
        return self.api.post(url=join_url(self._obj_url(pk), 'inquire/'), data=json.dumps({}))

    @function_log
    def fail(self, pk, reason):
        # type: (str, str) -> str
        url = join_url(self._obj_url(pk), 'fail/')
        return self.api.post(url=url, data=json.dumps({'reason': reason}))

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
            url=self._obj_url(pk),
            data=json.dumps({'asset': {'params': list_dict}}),
        )
