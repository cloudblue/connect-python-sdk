# -*- coding: utf-8 -*-

# This file is part of the CloudBlue Connect SDK.
# Copyright (c) 2025 CloudBlue. All Rights Reserved.

from .base import BaseModel
from .schemas import DocumentSchema


class Document(BaseModel):
    """ Document for a product. """

    _schema = DocumentSchema()

    title = None  # title: str
    """ (str) Document title. """

    url = None  # title: str
    """ (str) Document URL. """
