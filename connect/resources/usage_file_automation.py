# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from abc import ABCMeta

from connect.exceptions import SkipRequest, UsageFileAction
from connect.logger import logger
from connect.models import BaseModel, UsageFile, UsageFileSchema
from .automation_engine import AutomationEngine


class UsageFileAutomation(AutomationEngine):
    """ Automates workflow of Usage Files.

    For an example on how to use this class, see :ref:`usage_file_example`.
    """

    __metaclass__ = ABCMeta
    resource = 'usage/files'
    schema = UsageFileSchema(many=True)

    def dispatch(self, request):
        # type: (UsageFile) -> str
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
