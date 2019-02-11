# Connect Python  SDK

### Getting Started
---
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
### Example
```python
from config import Config
from resource.fulfillment import FulfillmentAutomation
from models.exception import FulfillmentFail, FulfillmentInquire, Skip

# You can set your credential or use a config file

# Example use the config file (recommend):
Config(file='config.json')

# Example set credential:
Config(
    api_url='https://api.connect.cloud.im/public/v1',
    api_key='ApiKey SU-520-000-000:57780e4760d2abbaa55d0a97354f6fb530000000',
    products='CN-631-322-000'
)


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
                                        'you decided to have an account in our amazing service!\n\n')
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

