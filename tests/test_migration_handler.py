# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
import os

from mock import patch, Mock, call

from connect.migration_handler import MigrationHandler
from connect.models import FulfillmentSchema
from connect.models.fulfillment import Fulfillment
from tests.common import load_str


def test_properties():
    # type: () -> None
    handler = MigrationHandler({})
    assert isinstance(handler, MigrationHandler)
    assert isinstance(handler.transformations, dict)
    assert isinstance(handler.migration_key, str)
    assert isinstance(handler.serialize, bool)
    assert len(handler.transformations) == 0
    assert handler.migration_key == 'migration_info'
    assert not handler.serialize


def test_needs_migration():
    # type: () -> None
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
    assert isinstance(requests_no_migration[0], Fulfillment)
    assert not handler._needs_migration(requests_no_migration[0])

    # Migration needed
    response_migration = load_str(os.path.join(
        os.path.dirname(__file__),
        'data',
        'request.migrate.valid.json'))
    request, error = FulfillmentSchema().loads(response_migration)
    assert not error
    assert isinstance(request, Fulfillment)
    assert handler._needs_migration(request)


@patch('connect.migration_handler.logger.info')
def test_no_migration(info_mock):
    # type: (Mock) -> None
    response = load_str(os.path.join(
        os.path.dirname(__file__),
        'data',
        'response.json'))
    requests, error = FulfillmentSchema().loads(response, many=True)
    assert not error
    assert isinstance(requests, list)
    assert len(requests) == 1

    handler = MigrationHandler({})
    request = handler.migrate(requests[0])
    info_mock.assert_called_once_with('[MIGRATION::PR-5852-1608-0000] Request does not need migration.')
    assert request == requests[0]


@patch('connect.migration_handler.logger.debug')
@patch('connect.migration_handler.logger.info')
def test_migration_skip_all(info_mock, debug_mock):
    # type: (Mock, Mock) -> None
    response = load_str(os.path.join(
        os.path.dirname(__file__),
        'data',
        'request.migrate.valid.json'))
    request, error = FulfillmentSchema().loads(response)

    handler = MigrationHandler({})
    migrated_request = handler.migrate(request)

    assert info_mock.call_count == 2
    info_mock.assert_has_calls([
        call('[MIGRATION::PR-7001-1234-5678] Running migration operations for request '
             'PR-7001-1234-5678'),
        call('[MIGRATION::PR-7001-1234-5678] 5 processed, 0 succeeded, 0 failed, 5 skipped '
             '(email, num_licensed_users, reseller_id, team_id, team_name).')
    ])

    assert debug_mock.call_count == 2
    debug_mock.assert_has_calls([
        call('[MIGRATION::PR-7001-1234-5678] Migration data `migration_info`: '
             '{"teamAdminEmail":"example.migration@mailinator.com",'
             '"teamId":"dbtid:AADaQq_w53nMDQbIPM_X123456PuzpcM2BI",'
             '"resellerId":["3ONEYO1234"],'
             '"teamName":"Migration Team",'
             '"licNumber":"10"}'),
        call('[MIGRATION::PR-7001-1234-5678] Migration data `migration_info` parsed correctly')
    ])

    assert migrated_request != request
    assert migrated_request.id == 'PR-7001-1234-5678'
    assert migrated_request.asset.id == 'AS-146-621-424-3'
    assert len(migrated_request.asset.params) == 6
    for i, _ in enumerate(migrated_request.asset.params):
        assert request.asset.params[i].id == migrated_request.asset.params[i].id
        assert request.asset.params[i].value == migrated_request.asset.params[i].value


"""
@patch('connect.migration_handler.logger.debug')
@patch('connect.migration_handler.logger.info')
def test_migration_wrong_info(info_mock, debug_mock):
    # type: (Mock, Mock) -> None
    response = load_str(os.path.join(
        os.path.dirname(__file__),
        'data',
        'request.migrate.invalid.json'))
    request, error = FulfillmentSchema().loads(response)
    if error:
        raise ValueError(error)

    handler = MigrationHandler({})
    migrated_request = handler.migrate(request)
"""