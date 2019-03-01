from connect.models import ActivationTemplateResponse, ActivationTileResponse
from .base import BaseResource
from .utils import joinurl


class TemplateResource(BaseResource):
    """ Specific resource.
    One method `render`
    He returns json string with activation tile
    """
    resource = 'templates'

    def render(self, pk, request_id):
        if not all([pk, request_id]):
            raise ValueError('Invalid ids for render temlpate')

        url = joinurl(self._obj_url(pk), 'render')
        response = self.api.get(url, params={'request_id': request_id})

        return ActivationTileResponse(response)

    def get(self, pk):
        return ActivationTemplateResponse(template_id=pk)

    def list(self):
        raise AttributeError('This resource do not have method `list`')
