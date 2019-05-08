Examples
********

Fulfillment processing
======================

 ::

    from connect.logger import logger
    from connect.models import ActivationTileResponse, FailRequest, InquireRequest, SkipRequest
    from connect.resource import FulfillmentAutomation, TierConfigAutomation


    class ExampleRequestProcessor(FulfillmentAutomation):
        def process_request(self, request):

            logger.info('Processing request {} for contract {}, product {}, marketplace {}'
                        .format(request.id,
                                request.contract.id,
                                request.asset.product.name,
                                request.marketplace.name))

            # Custom logic
            if request.type == 'purchase':
                for item in request.asset.items:
                    if item.quantity > 100000:
                        raise FailRequest(
                            message='Is Not possible to purchase product')

                for param in request.asset.params:
                    if param.name == 'email' and not param.value:
                        param.value_error = 'Email address has not been provided, please provide one'
                        raise InquireRequest(params=[param])

                # Approve by ActivationTile
                return ActivationTileResponse('\n  # Welcome to Fallball!\n\nYes, '
                                              'you decided to have an account in our amazing service!')
                # Or
                # return TemplateResource().render(pk='TEMPLATE_ID', request_id=request.id)

                # Approve by Template
                # return ActivationTemplateResponse('TL-497-535-242')
                # Or
                # return TemplateResource().get(pk='TEMPLATE_ID')

            elif request.type == 'change':
                # Fail
                raise FailRequest()
            else:
                # Skip request
                raise SkipRequest()

    class ExampleTierConfigProcessor(TierConfigAutomation):
        def process_request(self, request):
            pass


    if __name__ == '__main__':
        request_processor = ExampleRequestProcessor()
        request_processor.process()

        tier_config_processor = ExampleTierConfigProcessor()
        tier_config_processor.process()
