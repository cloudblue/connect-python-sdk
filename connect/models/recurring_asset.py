# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import RecurringAssetSchema

class RecurringAsset(BaseModel):
    """ RecurringAsset object. """

    _schema = RecurringAssetSchema()

    status = None  # type: ([)str)
    """ (vendor|provider) Billing Request status. """

    events = None  # type: obj
    """ (obj) Billing Request Events. """

    external_id = None  # type: (str)
    """ (str) External Id. """

    external_uuid = None  # type: (str)
    """ (str) External uuId. """

    product = None  # type: obj
    """ (obj) product. """

    connection = None  # type: obj
    """ (obj) Billing Request connection. """

    items = None  # type: obj
    """ (obj) Billing Request Item. """

    params = None  # type: obj
    """ (obj) Billing Request Params. """

    tiers = None  # type: obj
    """ (obj) Billing Request tiers. """

    marketplace = None  # type: obj
    """ (obj) Billing Request marketplace. """  
    
    contract = None  # type: obj
    """ (obj) Billing Request Contract. """

    billing = None  # type: obj
    """ (obj) Billing Request billing. """
