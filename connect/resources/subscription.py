from connect.config import Config
from connect.resources.billing_request import BillingRequestResource
from connect.resources.recurring_asset import RecurringAssetResource


class Subscription(object):
    """ Allows listing and obtaining several types of objects.

    :param Config config: Config object or ``None`` to use environment config (default).
    """

    _config = None  # type: Config

    def __init__(self, config=None):
        self._config = config or Config.get_instance()
        self._billing_request = BillingRequestResource(config=self._config)
        self._recurring_asset = RecurringAssetResource(config=self._config)

    def create_billing_request(self, obj):
        return self._billing_request.create(obj)

    def update_billing_request(self, pk, body):
        return self._billing_request.update_billing_request(pk,body)
