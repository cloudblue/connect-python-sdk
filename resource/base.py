from config import Config
from logger import log
import requests
from resource.utils import joinurl
from models import BaseScheme, ServerErrorSheme
from models.exception import ServerErrorException

config = Config()


class ApiClient(object):

    @property
    def headers(self):
        config.check_credentials(
            config.api_url, config.api_key, config.products)
        return {
            "Authorization": config.api_key,
            "Content-Type": "application/json",
        }

    def check_response(self, response):
        if not hasattr(response, 'content'):
            raise AttributeError(
                'Response not attribute content. Check your request params'
                'Response status - {}'.format(getattr(response, 'code')),
            )

        if not hasattr(response, 'ok') or not response.ok:
            data, error = ServerErrorSheme().loads(response.content)
            if data:
                raise ServerErrorException(data)

        return response.content

    @log
    def get(self, url, params=None, **kwargs):
        kwargs['headers'] = self.headers
        response = requests.get(url, params, **kwargs)
        return self.check_response(response)

    @log
    def post(self, url, data=None, json=None, **kwargs):
        kwargs['headers'] = self.headers
        response = requests.post(url, data, json, **kwargs)
        return self.check_response(response)

    @log
    def put(self, url, data=None, **kwargs):
        kwargs['headers'] = self.headers
        response = requests.put(url, data, **kwargs)
        return self.check_response(response)


class BaseResource(object):
    resource = None
    limit = 100
    api = ApiClient()
    scheme = BaseScheme()

    def __init__(self, *args, **kwargs):

        if self.__class__.resource is None:
            raise AttributeError('Resource name not specified in class {}'.format(
                self.__class__.__name__) + '. Add an attribute `resource` name of the resource')

    def build_filter(self):
        res_filter = {}
        if self.limit:
            res_filter['limit'] = self.limit

        return res_filter

    @property
    def _list_url(self):
        return joinurl(config.api_url, self.__class__.resource)

    def _obj_url(self, pk):
        return joinurl(self._list_url, pk)

    def __loads_sheme(self, response):
        objects, error = self.scheme.loads(response, many=True)
        if error:
            raise TypeError(
                'Invalid structure for initialisation objects. \n'
                'Error: {}. \nServer Response: {}'.format(error, response),
            )

        return objects

    @log
    def get(self, pk):
        response = self.api.get(url=self._obj_url(pk))
        objects = self.__loads_sheme(response)
        if isinstance(objects, list) and len(objects) > 0:
            return objects.data[0]

    @log
    def list(self):
        response = self.api.get(url=self._list_url, params=self.build_filter())
        return self.__loads_sheme(response)
