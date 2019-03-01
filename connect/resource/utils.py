# -*- coding: utf-8 -*-

from requests.compat import urljoin


def joinurl(base, url, allow_fragments=True):
    """ Method for the correct formation of the URL """
    if base and isinstance(base, str):
        base += '/' if base[-1] != '/' else ''
    return urljoin(base, url, allow_fragments=True)
