# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json


class ActivationTileResponse(object):
    tile = 'Activation succeeded'

    def __init__(self, markdown=None):
        if markdown:
            try:
                self.tile = json.loads(markdown)
            except ValueError:
                self.tile = markdown


class ActivationTemplateResponse(object):
    def __init__(self, template_id):
        self.template_id = template_id
