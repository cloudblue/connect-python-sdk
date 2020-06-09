import os
import unittest
import pytest
from mock import patch, MagicMock
from connect.exceptions import ServerError
from .common import Response, load_str

from connect.config import Config
from connect.resources.fulfillment import FulfillmentResource

create_tier_account_request_body = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'create_tier_account_request_body.json'))
create_tier_account_request_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'create_tier_account_request_response.json'))
create_purchase_request_body = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'create_purchase_request_body.json'))
create_purchase_request_response = load_str(
    os.path.join(os.path.dirname(__file__), 'data', 'create_purchase_request_response.json'))


class FulfillmentRequest(unittest.TestCase):
    def setUp(self):
        self.config = Config(file='tests/config.json')

    def _get_bad_response():
        return Response(
            ok=False,
            text='{}',
            status_code=404
        )

    @patch('requests.put')
    def test_update_param_asset_request(self, put_mock):
        request = FulfillmentResource(config=self.config)
        pr_id = 'PR-4405-9454-9305-001'
        test_data = {
            "params": [{
                "id": "PM-9861-7949-8492-0001",
                "value": "32323323"
            }]
        }
        request.update_param_asset_request(pr_id, test_data, "i'm a note!")
        assert put_mock.call_count == 1
        put_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            timeout=300,
            url=('http://localhost:8080/api/public/v1/'
                 'requests/PR-4405-9454-9305-001/'),
            json={
                'asset': test_data,
                'note': "i'm a note!",
            })

    @patch('requests.post')
    def test_create_tier_account_request(self, post_mock):
        post_mock.return_value = Response(True, create_tier_account_request_response, 200)
        body = create_tier_account_request_body
        request = FulfillmentResource(config=self.config)
        tier_account_request = request.create_tier_account_request(body)
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json=body,
            timeout=300,
            url='http://localhost:8080/api/public/v1/tier/account-requests')
        assert tier_account_request[0].id == 'TAR-6458-9737-0065-004-001'

    @patch('requests.get')
    def test_get_pending_tier_account(self, get_mock):
        get_mock.return_value = Response(True, create_tier_account_request_response, 200)
        request = FulfillmentResource(config=self.config)
        request.get_pending_tier_account_requests()
        get_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            params={'status': 'pending'},
            timeout=300,
            url='http://localhost:8080/api/public/v1/tier/account-requests')

    @patch('requests.get', MagicMock(return_value=_get_bad_response()))
    def test_search_pending_tier_account_bad(self):
        with pytest.raises(ServerError):
            request = FulfillmentResource(config=self.config)
            request.search_tier_account_requests(dict(status='pending'))

    @patch('requests.post')
    def test_create_purchase_request(self, post_mock):
        post_mock.return_value = Response(True, create_purchase_request_response, 200)
        body = create_purchase_request_body
        request = FulfillmentResource(config=self.config)
        purchase_request = request.create_purchase_request(body)
        post_mock.assert_called_with(
            headers={'Content-Type': 'application/json', 'Authorization': 'ApiKey XXXX:YYYYY'},
            json=body,
            timeout=300,
            url='http://localhost:8080/api/public/v1/requests')
        assert purchase_request.id == 'PR-9301-9893-8624-001'


if __name__ == "__main__":
    unittest.main()
