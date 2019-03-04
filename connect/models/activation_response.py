# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""

import json


class ActivationTileResponse(object):
    tile = None  # type: str

    def __init__(self, markdown=None):
        # type: (str) -> None
        try:
            self.tile = json.loads(markdown)
        except ValueError:
            self.tile = markdown or 'Activation succeeded'


class ActivationTemplateResponse(object):
    template_id = None  # type: str

    def __init__(self, template_id):
        # type: (str) -> None
        self.template_id = template_id
