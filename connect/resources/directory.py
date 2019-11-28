# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019 Ingram Micro. All Rights Reserved.

from connect.config import Config
from connect.models.asset import Asset
from connect.models.product import Product
from connect.models.tier_config import TierConfig
from connect.resources.base import ApiClient


class Directory(object):
    """ Allows listing and obtaining several types of objects.

    :param Config config: Config object or ``None`` to use environment config (default).
    """

    _config = None  # type: Config

    def __init__(self, config=None):
        self._config = config or Config.get_instance()

    def list_assets(self, filters=None):
        """ List the assets.

        :param (dict[str, Any] filters: Filters to pass to the request.
        :return: A list with the assets that match the given filters.
        :rtype: list[Asset]
        """
        products = ','.join(self._config.products) if self._config.products else None
        url = self._config.api_url + 'assets?in(product.id,(' + products + '))' \
            if products \
            else 'assets'
        text, code = ApiClient(self._config, url).get(params=filters)
        return Asset.deserialize(text)

    def get_asset(self, asset_id):
        """ Returns the asset with the given id.

        :param str asset_id: The id of the asset.
        :return: The asset with the given id, or ``None`` if such asset does not exist.
        :rtype: Asset|None
        """
        text, code = ApiClient(self._config, 'assets/' + asset_id).get()
        return Asset.deserialize(text)

    def list_products(self):
        """ List the products. Filtering is not possible at the moment.

        :return: A list with all products.
        :rtype: list[Product]
        """
        text, code = ApiClient(self._config, 'products').get()
        return Product.deserialize(text)

    def get_product(self, product_id):
        """ Returns the product with the given id.

        :param str product_id: The id of the product.
        :return: The product with the given id, or ``None`` if such product does not exist.
        :rtype: Product|None
        """
        text, code = ApiClient(self._config, 'products/' + product_id).get()
        return Product.deserialize(text)

    def list_tier_configs(self, filters=None):
        """ List the tier configs.

        :param (dict[str, Any] filters: Filters to pass to the request.
        :return: A list with the tier configs that match the given filters.
        :rtype: list[TierConfig]
        """
        filters = filters or {}
        products_key = 'product.id'
        if products_key not in filters and self._config.products:
            filters[products_key] = ','.join(self._config.products)
        text, code = ApiClient(self._config, 'tier/configs').get(params=filters)
        return TierConfig.deserialize(text)

    def get_tier_config(self, tier_config_id):
        """ Returns the tier config with the given id.

        :param str tier_config_id: The id of the tier config.
        :return: The Tier Config with the given id, or ``None`` if such Tier Config does not exist.
        :rtype: TierConfig|None
        """
        text, code = ApiClient(self._config, 'tier/configs/' + tier_config_id).get()
        return TierConfig.deserialize(text)
