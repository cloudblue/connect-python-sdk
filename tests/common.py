# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from collections import namedtuple
from typing import Optional
import json

Response = namedtuple('Response', ('ok', 'text', 'status_code'))
BinaryResponse = namedtuple('BinaryResponse', ('ok', 'content', 'status_code'))


def load_str(filename):
    # type: (str) -> Optional[str]
    try:
        with open(filename) as file_handle:
            return file_handle.read()
    except IOError:
        return None


def load_json(filename):
    try:
        with open(filename) as file_handle:
            return json.loads(file_handle.read())
    except IOError:
        return None
