# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from .base import BaseModel
from .schemas import ProductConfigurationSchema


class ProductConfiguration(BaseModel):
    """ Product configurations. """

    _schema = ProductConfigurationSchema()

    suspend_resume_supported = None  # type: bool
    """ (bool) Is suspend and resume supported for the product? """

    requires_reseller_information = None  # type: bool
    """ (bool) Does the product require reseller information? """
