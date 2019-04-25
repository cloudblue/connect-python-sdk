# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import copy
import json

import six
from typing import Dict

from connect.logger import logger
from connect.models.exception import Skip
from connect.models.fulfillment import Fulfillment


class MigrationAbortError(Exception):
    pass


class MigrationParamError(Exception):
    pass


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
                try:
                    parsed_data = json.loads(raw_data)
                except ValueError as ex:
                    raise MigrationAbortError(str(ex))
                logger.debug('[MIGRATION::{}] Migration data `{}` parsed correctly'
                             .format(request.id, self.migration_key))

                # These will keep track of processing status
                processed_params = []
                succeeded_params = []
                failed_params = []

                for param in request_copy.asset.params:
                    # Try to process the param and report success or fail
                    try:
                        if param.id in self.transformations:
                            # Transformation is defined, so apply it
                            logger.info('[MIGRATION::{}] Running transformation for parameter {}'
                                        .format(request.id, param.id))
                            param.value = self.transformations[param.id](parsed_data, request.id)
                        elif param.id in parsed_data:
                            # Parsed data contains the key, so assign it
                            if not isinstance(parsed_data[param.id], six.string_types):
                                if self.serialize:
                                    parsed_data[param.id] = json.loads(parsed_data[param.id])
                                else:
                                    type_name = type(parsed_data[param.id]).__name__
                                    raise MigrationParamError(
                                        'Parameter {} type must be str, but {} was given'
                                        .format(param.id, type_name))
                            param.value = parsed_data[param.id]
                        succeeded_params.append(param.id)
                    except MigrationParamError as ex:
                        logger.error('[MIGRATION::{}] {}'.format(request.id, ex))
                        failed_params.append(param.id)

                    # Report processed param
                    processed_params.append(param.id)

                    # Raise abort if any params failed
                    if failed_params:
                        raise MigrationAbortError(
                            'Processing of parameters {} failed, unable to complete migration.'
                            .format(', '.join(failed_params)))

                    logger.info('[MIGRATION::{}] Parameters {}/{} ({}) processed correctly.'
                                .format(
                                    request.id,
                                    len(succeeded_params),
                                    len(processed_params),
                                    ', '.join(succeeded_params)))
            except MigrationAbortError as ex:
                logger.error('[MIGRATION::{}] {}'.format(request.id, ex))
                raise Skip('Migration failed.')

            return request_copy
        else:
            logger.info('[MIGRATION::{}] Request does not need migration.'
                        .format(request.id))
            return request

    def _needs_migration(self, request):
        # type: (Fulfillment) -> bool
        return request.asset.get_param_by_id(self.migration_key) is not None
