# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import UsageRecordSchema


class UsageRecord(BaseModel):
    """ Usage Record Object. """

    _schema = UsageRecordSchema()

    usage_record_id = None  # type: str
    """ (str) Usage record id. """

    item_search_criteria = None  # type: str
    """ (str) Item search criteria. """

    item_search_value = None  # type: str
    """ (str) Item search value. """

    quantity = None  # type: int
    """ (int) Quantity. """

    start_time_utc = None  # type: str
    """ (str) Start Time in UTC. """

    end_time_utc = None  # type: str
    """ (str) End Time in UTC. """

    asset_search_criteria = None  # type: str
    """ (str) Asset search criteria. """

    asset_search_value = None  # type: str
    """ (str) Asset search value. """
