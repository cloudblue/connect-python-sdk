# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import sys
import logging
from abc import ABCMeta

from connect.exceptions import SkipRequest, UsageFileAction
from connect.logger import logger as global_logger
from connect.models import BaseModel, UsageFile
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
            filters['product__id'] = ','.join(self.config.products)
        return filters

    def dispatch(self, request):
        # type: (UsageFile) -> str
        handlers = global_logger.handlers
        handlers.append(logging.StreamHandler(sys.stdout))
        log_level = global_logger.level
        self.__class__.logger.setLevel(log_level)
        [self.__class__.logger.addHandler(hdlr) for hdlr in handlers]
        base = " %(levelname)-6s; %(asctime)s; %(name)-6s; %(module)s:%(funcName)s:line" \
               "-%(lineno)d: %(message)s"
        sformat = request.marketplace.id + "  " + request.id + base
        [handler.setFormatter(logging.Formatter(sformat, "%I:%M:%S"))
         for handler in self.logger.handlers]

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
                json=usage.obj.json
                if isinstance(usage.obj, BaseModel)
                else getattr(usage.obj, '__dict__', str(usage.obj)))
            processing_result = usage.code

        # Catch skip
        except SkipRequest:
            processing_result = 'skip'

        self.logger.info('Finished processing of usage file with ID {} with result {}'
                         .format(request.id, processing_result))
        return processing_result
