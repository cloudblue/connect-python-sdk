# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from abc import ABCMeta

from connect.logger import logger
from connect.models.base import BaseModel
from connect.models.exception import UsageFileAction, SkipRequest
from connect.models.usage import FileSchema, File
from .automation import AutomationResource


class UsageFileAutomation(AutomationResource):
    __metaclass__ = ABCMeta
    resource = 'usage/files'
    schema = FileSchema(many=True)

    def dispatch(self, request):
        # type: (File) -> str
        try:
            # Validate product
            if self.config.products \
                    and request.product.id not in self.config.products:
                return 'Invalid product'

            # Process request
            logger.info(
                'Start usage file request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            # Report that expected exception was not raised
            processing_result = 'UsageFileAutomation.process_request returned {} while ' \
                                'is expected to raise UsageFileAction or SkipRequest exception' \
                .format(str(result))
            logger.warning(processing_result)
            raise UserWarning(processing_result)

        # Catch action
        except UsageFileAction as usage:
            self._api.post(
                path='{}/{}'.format(request.id, usage.code),
                json=usage.obj.json
                if isinstance(usage.obj, BaseModel)
                else getattr(usage.obj, '__dict__', str(usage.obj)))
            processing_result = usage.code

        # Catch skip
        except SkipRequest:
            processing_result = 'skip'

        logger.info('Finished processing of usage file with ID {} with result {}'
                    .format(request.id, processing_result))
        return processing_result
