from .fulfillment import FulfillmentResource

from models import ActivationTemplateResponse, ActivationTileResponse
from models.exception import Skip, FulfillmentFail, FulfillmentInquire


class FulfillmentAutomation(FulfillmentResource):

    def process(self):
        for _ in self.list():
            self.dispatch(_)

    def dispatch(self, request):
        try:
            result = self.process_request(request)

            if not result:
                # TODO write log info
                return

            params = {}
            if isinstance(result, ActivationTileResponse):
                params = {'activation_tile': result.tile}
            elif isinstance(result, ActivationTemplateResponse):
                params = {'template_id': result.template_id}

            if not params:
                # TODO write log info
                return

            self.approve(request.id, params)

        except FulfillmentInquire as inquire:
            # TODO write log info
            self.update_parameters(request.id, inquire.params)
            return self.inquire(request.id)

        except FulfillmentFail as fail:
            # TODO write log info
            return self.fail(request.id, reason=fail.message)

        except Skip as skip:
            # TODO write log info
            return skip.code
        return

    def process_request(self, request):
        raise NotImplementedError(
            'Please implementation `process_request` logic')
