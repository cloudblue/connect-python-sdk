# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import RecurringAssetSchema


class RecurringAsset(BaseModel):
    """ RecurringAsset object. """

    _schema = RecurringAssetSchema()

    status = None  # type: (str)
    """ (vendor|provider) Billing Request status. """

    events = None  # type: (object)
    """ (object) Billing Request Events. """

    external_id = None  # type: (str)
    """ (str) External Id. """

    external_uuid = None  # type: (str)
    """ (str) External uuId. """

    product = None  # type: (object)
    """ (object) product. """

    connection = None  # type: (object)
    """ (object) Billing Request connection. """

    items = None  # type: (object)
    """ (object) Billing Request Item. """

    params = None  # type: (object)
    """ (object) Billing Request Params. """

    tiers = None  # type: (object)
    """ (object) Billing Request tiers. """

    marketplace = None  # type: (object)
    """ (object) Billing Request marketplace. """

    contract = None  # type: (object)
    """ (object) Billing Request Contract. """

    billing = None  # type: (object)
    """ (object) Billing Request billing. """
