# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from copy import copy

from connect.config import Config
from connect.models.asset import Asset
from connect.models.product import Product
from connect.models.tier_config import TierConfig
from connect.resources.base import ApiClient
from connect.resources.marketplace import MarketplaceResource
from connect.resources.tier_account import TierAccountResource
from connect.rql import Query


class Directory(object):
    """ Allows listing and obtaining several types of objects.

    :param Config config: Config object or ``None`` to use environment config (default).
    """

    _config = None  # type: Config

    def __init__(self, config=None):
        self._config = config or Config.get_instance()
        self._tier_accounts = TierAccountResource(config=self._config)

    def list_assets(self, filters=None):
        """ List the assets.

        :param dict|Query filters: Filters to pass to the request.
        :return: A list with the assets that match the given filters.
        :rtype: list[Asset]
        """
        query = self._get_filters_query(filters, True)
        text, code = ApiClient(self._config, 'assets' + query.compile()).get()
        return Asset.deserialize(text)

    def get_asset(self, asset_id):
        """ Returns the asset with the given id.

        :param str asset_id: The id of the asset.
        :return: The asset with the given id, or ``None`` if such asset does not exist.
        :rtype: Asset|None
        """
        text, code = ApiClient(self._config, 'assets/' + asset_id).get()
        return Asset.deserialize(text)

    def list_marketplaces(self, filters=None):
        """ List the marketplaces.

        :param dict|Query filters: Filters to pass to the request.
        :return: List of marketplaces matching given filters.
        :rtype: list[Marketplace]
        """
        return MarketplaceResource(self._config).list(filters)

    def get_marketplace(self, marketplace_id):
        """ Obtains Marketplace object given its ID.

        :param str marketplace_id: The id of the marketplace.
        :return: The marketplace with the given id, or ``None`` if such marketplace does not exist.
        :rtype: Marketplace|None
        """
        return MarketplaceResource(self._config).get(marketplace_id)

    def list_products(self, filters=None):
        """ List the products.

        :param dict|Query filters: Filters to pass to the request.
        :return: A list with all products.
        :rtype: list[Product]
        """
        query = self._get_filters_query(filters, False)
        text, code = ApiClient(self._config, 'products' + query.compile()).get()
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
        query = self._get_filters_query(filters, True)
        text, code = ApiClient(self._config, 'tier/configs' + query.compile()).get()
        return TierConfig.deserialize(text)

    def get_tier_config(self, tier_config_id):
        """ Returns the tier config with the given id.

        :param str tier_config_id: The id of the tier config.
        :return: The Tier Config with the given id, or ``None`` if such Tier Config does not exist.
        :rtype: TierConfig|None
        """
        text, code = ApiClient(self._config, 'tier/configs/' + tier_config_id).get()
        return TierConfig.deserialize(text)

    def _get_filters_query(self, filters, add_product):
        """
        :param dict|Query filters: Filters to return as query (with product.id field).
        :param bool add_product: Whether to add a product.id field to the query.
        :return: The query.
        :rtype: Query
        """
        query = copy(filters) if isinstance(filters, Query) else Query(filters)
        if add_product and self._config.products:
            query.in_('product.id', self._config.products)
        return query

    def search_tier_accounts(self, filters):
        return self._tier_accounts.search(filters)

    def get_tier_account(self, pk):
        return self._tier_accounts.get(pk)
