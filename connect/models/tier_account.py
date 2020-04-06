# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import TierAccountSchema


class TierAccount(BaseModel):
    """ Tier account. """

    _schema = TierAccountSchema()

    name = None
    contact_info = None
    external_id = None
    external_uid = None
    environment = None
    marketplace = None
    hub = None
    version = None
    events = None
    scopes = None
