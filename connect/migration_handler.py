# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import copy
import json

from typing import Dict

from connect.logger import logger
from connect.models.fulfillment import Fulfillment


class MigrationHandler(object):
    def __init__(self, transformations, migration_key='migration_info', serialize=False):
        # type: (Dict[str, callable], str, bool) -> None
        self._transformations = transformations
        self._migration_key = migration_key
        self._serialize = serialize

    @property
    def transformations(self):
        # type: () -> Dict[str, callable]
        return self._transformations

    @property
    def migration_key(self):
        # type: () -> str
        return self._migration_key

    @property
    def serialize(self):
        # type: () -> bool
        return self._serialize

    def migrate(self, request):
        # type: (Fulfillment) -> Fulfillment
        if self._needs_migration(request):
            logger.info('[MIGRATION::{}] Running migration operations for request {}'
                        .format(request.id, request.id))
            request_copy = copy.deepcopy(request)

            raw_data = request.asset.get_param_by_id(self.migration_key).value
            logger.debug('[MIGRATION::{}] Migration data `{}`: {}'
                         .format(request.id, self.migration_key, raw_data))

            try:
                # This will raise a ValueError if parsing fails
                parsed_data = json.loads(raw_data)
                logger.debug('[MIGRATION::{}] Migration data `{}` parsed correctly'
                             .format(request.id, self.migration_key))

                for param in request_copy.asset.params:
                    if param.id in self.transformations:
                        # Transformation operation is registered, so transform property
                        logger.info('[MIGRATION::{}] Running transformation for parameter {}'
                                    .format(request.id, param.id))
                        param.value = self.transformations[param.id](parsed_data, request.id)
                    else:
                        pass
            except ValueError:
                pass
        else:
            logger.info('[MIGRATION::{}] Request does not need migration'
                        .format(request.id))
            return request

    def _needs_migration(self, request):
        # type: (Fulfillment) -> bool
        return request.asset.get_param_by_id(self.migration_key) is not None
