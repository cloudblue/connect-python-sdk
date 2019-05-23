# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from collections import namedtuple

from typing import Optional

Response = namedtuple('Response', ('ok', 'content', 'status_code'))


def load_str(filename):
    # type: (str) -> Optional[str]
    try:
        with open(filename) as file_handle:
            return file_handle.read()
    except IOError:
        return None
