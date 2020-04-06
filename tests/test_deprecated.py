# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

import pytest

from connect.exceptions import Message


def test_deprecated_message():
    # type: () -> None
    with pytest.deprecated_call():
        # noinspection PyStatementEffect
        Message('Hello').message
