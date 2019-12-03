from mock import patch, call
from connect.logger import function_log
from connect.config import Config

test_value = 1
test_dictionary_1 = {
    "apiEndpoint": "www.ingrammicro.com",
    "apiKey": "fakeApiKey 123456",
    "products": "fakeProduct"
}


@function_log(config=Config.get_instance())
def hidden_logger(value1, value2):
    return value1, value2


@patch("logging.Logger.debug")
def test_hidden_logger(debug_mock):
    hidden_logger(test_value, test_dictionary_1)
    assert debug_mock.call_count == 2
    debug_mock.assert_has_calls([
        call(
            "Function params: ({'apiEndpoint': 'www.ingrammicro.com', 'apiKey': '*****************', 'products': 'fakeProduct'},) {}"),
        call(
            "Function `int.hidden_logger` return: (1, {'apiEndpoint': 'www.ingrammicro.com', 'apiKey': '*****************', 'products': 'fakeProduct'})")
    ])
