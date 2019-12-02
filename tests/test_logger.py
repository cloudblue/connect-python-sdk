from connect.logger import function_log
from connect.config import Config

test_dictionary_1 = {
    "apiEndpoint": "value to display",
    "apiKey": "value to display",
    "products": "value to display",
    "log_level": "value to display",
    "service": {
        "environment": "value to display",
        "partnerConfig": {
            "MP-00000": {
                "m1": "value to display",
                "m2": "value to display",
                "m3": "value to display"
            }
        },
        "executionPort": 8000,
        "log_file_name": "value to display",
        "actionsSecret": "value to display"
    }
}

test_dictionary_2 = {
    "apiEndpoint": "value to display",
    "apiKey2": "value to display",
    "products": "value to display",
    "log_level": "value to display",
    "service": {
        "environment": "value to display",
        "partnerConfig": {
            "MP-00000": {
                "m1": "value to display",
                "m2": "value to display",
                "m3": "value to display"
            }
        },
        "executionPort": 8000,
        "log_file_name": "value to display",
        "actionsSecret": "value to display"
    }
}

test_int_value_1 = 10000
test_str_value_1 = "test value"


class TestLogger:

    @function_log(config=Config.get_instance())
    def test_logger(self, value1, value2, value3):
        return value1, value2, value3


TestLogger().test_logger(test_int_value_1, test_dictionary_2, value3=test_dictionary_1)
