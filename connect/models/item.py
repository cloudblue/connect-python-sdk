# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from typing import List, Optional, Union

from .base import BaseModel
from .commitment import Commitment
from .param import Param
from .renewal import Renewal
from .schemas import ItemSchema
from .ui import UI
from .unit import Unit


class Item(BaseModel):
    """ A product item. """

    _schema = ItemSchema()

    mpn = None  # type: str
    """ (str) Item manufacture part number. """

    quantity = None  # type: Union[int,float]
    """ (int|float) Number of items of the type in the asset (-1 if unlimited) """

    old_quantity = None  # type: Union[int,float,None]
    """ (int|float|None) Previous value of quantity. """

    renewal = None  # type: Optional[Renewal]
    """ (:py:class:`.Renewal` | None) Parameters of renewal request
    (empty for all other types).
    """

    params = None  # type: List[Param]
    """ (List[:py:class:`.Param` | None] List of Item and Item x Marketplace Configuration Phase
    Parameter Context-Bound Object
    """

    # Undocumented fields (they appear in PHP SDK)

    display_name = None  # type: str
    """ (str) Display name. """

    global_id = None  # type: str
    """ (str) Global id. """

    item_type = None  # type: str
    """ (str) Item type. """

    period = None  # type: str
    """ (str) Period. """

    type = None  # type: str
    """ (str) Type. """

    name = None  # type: str
    """ (str) Name. """

    unit = None  # type: Unit
    """ (Unit) Measure unit. """

    commitment = None  # type: Optional[Commitment]
    """ (Commitment) item billing commitment. """

    ui = None  # type: UI
    """ (UI) UI visibility. """

    def get_param_by_id(self, param_id):
        """ Get a parameter of the item.

        :param str param_id: Id of the the parameter to get.
        :return: The parameter with the given id, or ``None`` if it was not found.
        :rtype: :py:class:`.Param` | None
        """
        try:
            return list(filter(lambda param: param.id == param_id, self.params))[0]
        except IndexError:
            return None
