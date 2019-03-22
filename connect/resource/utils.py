# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

from requests.compat import urljoin


def join_url(base, url, allow_fragments=True):
    # type: (str, str, bool) -> str
    """ Method for the correct formation of the URL """
    if base and isinstance(base, str):
        base += '/' if base[-1] != '/' else ''
    return urljoin(base, url, allow_fragments=allow_fragments)
