from config import Config
from resource import FulfillmentAutomation, TemplateResource
from models.exception import FulfillmentFail, FulfillmentInquire, Skip
from models import ActivationTileResponse, ActivationTemplateResponse


Config(file='config.json')


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
