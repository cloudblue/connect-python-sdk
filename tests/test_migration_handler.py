# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import os

from mock import patch

from connect.migration_handler import MigrationHandler
from connect.models import FulfillmentSchema
from tests.common import load_str


def test_properties():
    handler = MigrationHandler({})
    assert isinstance(handler, MigrationHandler)
    assert isinstance(handler.transformations, dict)
    assert isinstance(handler.migration_key, str)
    assert isinstance(handler.serialize, bool)
    assert len(handler.transformations) == 0
    assert handler.migration_key == 'migration_info'
    assert not handler.serialize


def test_needs_migration():
    handler = MigrationHandler({})

    # No migration needed
    response_no_migration = load_str(os.path.join(
        os.path.dirname(__file__),
        'data',
        'response.json'))
    requests_no_migration, error = FulfillmentSchema().loads(response_no_migration, many=True)
    assert not error
    assert isinstance(requests_no_migration, list)
    assert len(requests_no_migration) == 1
    assert not handler._needs_migration(requests_no_migration[0])


@patch('connect.migration_handler.logger')
def test_no_migration(_):
    response_no_migration = load_str(os.path.join(
        os.path.dirname(__file__),
        'data',
        'response.json'))
    requests_no_migration, error = FulfillmentSchema().loads(response_no_migration, many=True)
    assert not error
    assert isinstance(requests_no_migration, list)
    assert len(requests_no_migration) == 1

    handler = MigrationHandler({})
    handler.migrate(requests_no_migration[0])
