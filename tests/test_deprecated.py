# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import pytest

from mock import patch
from connect.exceptions import Message
from connect.resources.base import BaseResource
from .common import Response


def test_deprecated_message():
    # type: () -> None
    with pytest.deprecated_call():
        # noinspection PyStatementEffect
        Message('Hello').message


@patch('requests.get')
def test_deprecation_filter_in(get_mock):
    get_mock.return_value = Response(True, '[]', 200)

    class TestResource(BaseResource):
        resource = 'test'

    test_resouce = TestResource()
    filters = {
        'deprecated__in': (1, 2)
    }
    with pytest.deprecated_call() as warning:
        test_resouce.search(filters)
    assert str(warning[0].message) == 'deprecated__in: __in operator is deprecated, Use RQL syntax'
