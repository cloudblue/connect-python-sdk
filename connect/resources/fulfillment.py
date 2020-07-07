from connect.config import Config
from connect.resources.tier_account import TierAccountRequestResource
from connect.resources.tier_config_request import TierConfigRequestResource
from connect.resources.asset_request import AssetRequestResource


class FulfillmentResource(object):
    """ Allows listing and obtaining several types of objects.
        :param Config config: Config object or ``None`` to use environment config (default).
    """

    _config = None  # type: Config

    def __init__(self, config=None):
        self._config = config or Config.get_instance()
        self._tier_account_requests = TierAccountRequestResource(config=self._config)
        self._tier_config_requests = TierConfigRequestResource(config=self._config)
        self._asset_requests = AssetRequestResource(config=self._config)

    def create_tier_account_request(self, obj):
        return self._tier_account_requests.create(obj)

    def accept_tier_account_request(self, id_tar):
        return self._tier_account_requests.accept(id_tar)

    def ignore_tier_account_request(self, id_tar, reason):
        return self._tier_account_requests.ignore(id_tar, reason)

    def get_pending_tier_account_requests(self):
        return self._tier_account_requests.search(dict(status='pending'))

    def search_tier_account_requests(self, filters):
        return self._tier_account_requests.search(filters)

    def update_param_asset_request(self, request_id, data, note=None):
        return self._asset_requests.update_param_asset_request(request_id, data, note)

    def create_purchase_request(self, obj):
        return self._asset_requests.create(obj)

    def search_asset_request(self, obj):
        return self._asset_requests.search(obj)
