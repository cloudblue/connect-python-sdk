from connect.config import Config
from connect.resources.tier_account import TierAccountRequestResource

class Fulfillment(object):
    """ Allows listing and obtaining several types of objects.

    :param Config config: Config object or ``None`` to use environment config (default).
    """

    _config = None  # type: Config

    def __init__(self, config=None):
        self._config = config or Config.get_instance()
        self._tier_account_requests = TierAccountRequestResource(config=self._config)

    def create_tier_account_request(self, obj):
        return self._tier_account_requests.create(obj)

    def accept_tier_account_request(self, pk):
        return self._tier_account_requests.accept(pk)

    def ignore_tier_account_request(self, pk, reason):
        return self._tier_account_requests.ignore(pk, reason)

    def get_pending_tier_account_requests(self):
        return self._tier_account_requests.search(dict(status='pending'))

    def create_purchase_request(self, obj):
        pass