# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

import json


class ActivationTileResponse(object):
    """ An instance of this class might the returned by the overriden ``process_request`` method
    of your :py:class:`connect.resources.FulfillmentAutomation` or
    :py:class:`connect.resources.TierConfigAutomation` subclass to approve the request being
    processed, showing a tile with the specified contents.

    :param str markdown: Contents of the tile to be shown in the Vendor Portal, in Markdown format.
    :rtype: None
    """

    tile = 'Activation succeeded'  # type: str

    def __init__(self, markdown=''):
        try:
            self.tile = json.loads(markdown)
        except ValueError:
            self.tile = markdown or self.__class__.tile


class ActivationTemplateResponse(object):
    """ An instance of this class might the returned by the overriden ``process_request`` method
    of your :py:class:`connect.resources.FulfillmentAutomation` or
    :py:class:`connect.resources.TierConfigAutomation` subclass to approve the request being
    processed, showing a tile with the specified template id.

    :param str template_id: Id of the template od the tile to be shown in the Vendor Portal.
        The template must have been defined in the Vendor Portal.
    :rtype: None
    """

    template_id = None  # type: str

    def __init__(self, template_id):
        self.template_id = template_id
