# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import json
import logging
from abc import ABCMeta

from connect.exceptions import SkipRequest, UsageFileAction
from connect.models.base import BaseModel
from connect.models.usage_file import UsageFile
from .automation_engine import AutomationEngine


class UsageFileAutomation(AutomationEngine):
    """ Automates workflow of Usage Files.

    For an example on how to use this class, see :ref:`usage_file_example`.
    """

    __metaclass__ = ABCMeta
    resource = 'usage/files'
    model_class = UsageFile
    logger = logging.getLogger('UsageFile.logger')

    def filters(self, status='ready', **kwargs):
        """
        :param str status: Status of the requests. Default: ``'ready'``.
        :param dict[str,Any] kwargs: Additional filters to add to the default ones.
        :return: The set of filters for this resource.
        :rtype: dict[str,Any]
        """
        filters = super(UsageFileAutomation, self).filters(status, **kwargs)
        if self.config.products:
            filters['product_id__in'] = ','.join(self.config.products)
        return filters

    def dispatch(self, request):
        # type: (UsageFile) -> str

        self._set_custom_logger(request.id, request.name)

        try:
            # Validate product
            if self.config.products \
                    and request.product.id not in self.config.products:
                return 'Invalid product'

            # Process request
            self.logger.info(
                'Start usage file request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            # Report that expected exception was not raised
            processing_result = 'UsageFileAutomation.process_request returned {} while ' \
                                'is expected to raise UsageFileAction or SkipRequest exception' \
                .format(str(result))
            self.logger.warning(processing_result)
            raise UserWarning(processing_result)

        # Catch action
        except UsageFileAction as usage:
            self._api.post(
                path='{}/{}'.format(request.id, usage.code),
                data=json.dumps(usage.obj.json
                                if isinstance(usage.obj, BaseModel)
                                else usage.obj))
            processing_result = usage.code

        # Catch skip
        except SkipRequest:
            processing_result = 'skip'

        self.logger.info('Finished processing of usage file with ID {} with result {}'
                         .format(request.id, processing_result))
        return processing_result
