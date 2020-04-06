# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import os

from connect.models import ServerErrorResponse
from .common import load_str


server_error_response_content = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'response_server_error.json'))


def test_server_error_response_attributes():
    # type: () -> None
    srv_error = ServerErrorResponse.deserialize(server_error_response_content)
    assert isinstance(srv_error, ServerErrorResponse)
    assert srv_error.error_code == 'ERR_000'
    assert isinstance(srv_error.errors, list)
    assert len(srv_error.errors) == 2
    assert isinstance(srv_error.params, dict)
