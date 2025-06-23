# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import DownloadLinkSchema


class DownloadLink(BaseModel):
    """ Download link for a product. """

    _schema = DownloadLinkSchema()

    title = None  # type: str
    """ (str) Link title. """

    url = None  # type: str
    """ (str) Link URL. """

    visible_for = None  # title: str
    """ (str) Link visibility. One of: admin, user. """
