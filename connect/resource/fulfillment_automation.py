from connect.logger import logger
from connect.models import ActivationTemplateResponse, ActivationTileResponse
from connect.models.exception import FulfillmentFail, FulfillmentInquire, Skip
from .fulfillment import FulfillmentResource


class FulfillmentAutomation(FulfillmentResource):

    def process(self):
        for _ in self.list():
            self.dispatch(_)

    def dispatch(self, request):
        try:
            logger.info('Start request process / ID request - {}'.format(request.id))
            result = self.process_request(request)

            if not result:
                logger.info('Method `process_request` did not return result')
                return

            params = {}
            if isinstance(result, ActivationTileResponse):
                params = {'activation_tile': result.tile}
            elif isinstance(result, ActivationTemplateResponse):
                params = {'template_id': result.template_id}

            self.approve(request.id, params)

        except FulfillmentInquire as inquire:
            self.update_parameters(request.id, inquire.params)
            return self.inquire(request.id)

        except FulfillmentFail as fail:
            return self.fail(request.id, reason=fail.message)

        except Skip as skip:
            return skip.code
        return

    def process_request(self, request):
        raise NotImplementedError(
            'Please implementation `process_request` logic')
