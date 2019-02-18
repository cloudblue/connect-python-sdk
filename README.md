# Connect Python  SDK

![pyversions](https://img.shields.io/pypi/pyversions/connect-sdk.svg)  [![PyPi Status](https://img.shields.io/pypi/v/connect-sdk.svg)](https://pypi.org/project/connect-sdk/) [![codecov](https://codecov.io/gh/ingrammicro/connect-python-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/ingrammicro/connect-python-sdk) [![Build Status](https://travis-ci.org/ingrammicro/connect-python-sdk.svg?branch=master)](https://travis-ci.org/ingrammicro/connect-python-sdk) [![PyPI status](https://img.shields.io/pypi/status/connect-sdk.svg)](https://pypi.python.org/pypi/connect-sdk/)
### Getting Started
---
Connect Python SDK allows an easy and fast integration with Connect fulfillment API. Thanks to it you can automate the fulfillment of orders generated by your products.

In order to use this library, please ensure that you have read first the documentation available on Connect knowladge base article located here, this one will provide you a great information on the rest api that this library implements.
### Class Features
---
This library may be consumed in your project in order to automate the fulfillment of requests, this class once imported into your project will allow you to:

- Connect to Connect using your api credentials
- List all requests, and even filter them:
    - for a Concrete product
    - for a concrete status
- Process each request and obtain full details of the request
- Modify for each request the activation parameters in order to:
    - Inquiry for changes
    - Store information into the fulfillment request
- Change the status of the requests from it's initial pending state to either inquiring, failed or approved.
- Generate logs
- Collect debug logs in case of failure

Your code may use any scheduler to execute, from a simple cron to a cloud scheduler like the ones available in Azure, Google, Amazon or other cloud platforms.

### Installation

```sh
$ pip install connect-sdk
```

### Requirements
* Python 2.7+ or Python 3.4+
* Requests (https://pypi.org/project/requests/)
* Marshmallow (https://pypi.org/project/marshmallow/)

### Example
```python
from connect import FulfillmentAutomation
from connect.config import Config
from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip

Config(file='config.json')

# set logger level / default level ERROR
logger.setLevel("DEBUG")


class ExampleRequestProcessor(FulfillmentAutomation):
    def process_request(self, request):

        # custom logic
        if request.type == 'purchase':
            for item in request.asset.items:
                if item.quantity > 100000:
                    raise FulfillmentFail(
                        message='Is Not possible to purchase product')

            for param in request.asset.params:
                if param.name == 'email' and not param.value:
                    param.value_error = 'Email address has not been provided, please provide one'
                    raise FulfillmentInquire(params=[param])

            # approve by ActivationTile
            return ActivationTileResponse(tile='\n  # Welcome to Fallball!\n\nYes, '
                                               'you decided to have an account in our amazing service!')
            # or
            # return TemplateResource().render(pk='TEMPLATE_ID', request_id=request.id)

            # aprrove by Template
            return ActivationTemplateResponse(template_id="TL-497-535-242")
            # or
            # return TemplateResource().get(pk='TEMPLATE_ID')

        elif request.type == 'change':
            # fail
            raise FulfillmentFail()
        else:
            # skip request
            raise Skip()


if __name__ == '__main__':
    request = ExampleRequestProcessor()
    request.process()
```

