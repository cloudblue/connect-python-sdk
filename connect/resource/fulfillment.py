# -*- coding: utf-8 -*-

import json

from connect.config import Config
from connect.logger import function_log
from connect.models import FulfillmentScheme, Param
from .base import BaseResource
from .template import TemplateResource
from .utils import joinurl


class FulfillmentResource(BaseResource):
    resource = 'requests'
    limit = 1000
    scheme = FulfillmentScheme()

    def build_filter(self):
        filters = super(FulfillmentResource, self).build_filter()
        if Config.products:
            filters['product_id'] = Config.products

        filters['status'] = 'pending'
        return filters

    @function_log
    def approve(self, pk, data):
        url = joinurl(self._obj_url(pk), 'approve/')
        return self.api.post(url=url, data=json.dumps(data if data else {}))

    @function_log
    def inquire(self, pk):
        return self.api.post(url=joinurl(self._obj_url(pk), 'inquire/'), data=json.dumps({}))

    @function_log
    def fail(self, pk, reason):
        url = joinurl(self._obj_url(pk), 'fail/')
        return self.api.post(url=url, data=json.dumps({'reason': reason}))

    @function_log
    def render_template(self, pk, template_id):
        return TemplateResource().render(template_id, pk)

    @function_log
    def update_parameters(self, pk, params):
        list_dict = []
        for _ in params:
            list_dict.append(_.__dict__ if isinstance(_, Param) else _)

        return self.api.put(
            url=self._obj_url(pk),
            data=json.dumps({'asset': {'params': list_dict}}),
        )
