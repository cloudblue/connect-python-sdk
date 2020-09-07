import json

from .base import BaseResource, NestedResource
from ..models import Product, Item


class ProductItemResource(NestedResource):
    resource = 'items'
    model_class = Item


class ProductsResource(BaseResource):
    """ Allows listing and obtaining several types of objects.
        :param Config config: Config object or ``None`` to use environment config (default).
    """
    resource = 'products'
    model_class = Product

    def list_parameters(self, product_id):
        """ List parameters for a product.
        :param str product_id: Primary key of the product to search for.
        :return: response object with templates contents.
        """
        """
        # type: (Dict[str, Any]) -> List[Any]
        """
        response, _ = self._api.get(
            '/public/v1/products/' + product_id + '/parameters/'
        )
        response = json.loads(response)
        return response

    def create_parameter(self, product_id, body):
        """ Create parameter for a product.
        :param str product_id: Primary key of the product to create parameter.
        :param str body: Body of the parameter to create.
        :return: response object with templates contents.
        """
        """
        # type: (Dict[str, Any]) -> List[Any]
        """
        if not product_id:
            raise ValueError('Invalid ID')
        path = '/public/v1/products/' + product_id + '/parameters/'
        response = self._api.post(
            path=path,
            json=body
        )
        return response

    def update_parameter(self, product_id, parameter_id, body):
        """ Update parameter for a product.
        :param str product_id: Primary key of the product to update parameter.
        :param str parameter_id: Primary key of the parameter to update.
        :param str body: Body of the parameter to update.
        :return: response object with templates contents.
        """
        """
        # type: (Dict[str, Any]) -> List[Any]
        """
        if not product_id:
            raise ValueError('Invalid ID')
        path = '/public/v1/products/' + product_id + '/parameters/' + parameter_id
        response = self._api.put(
            path=path,
            json=body
        )
        return response

    def delete_parameter(self, product_id, parameter_id):
        """ Delete parameter for a product.
        :param str product_id: Primary key of the product to delete parameter.
        :param str parameter_id: Primary key of the parameter to delete.
        :return: response object with templates contents.
        """
        """
        # type: (Dict[str, Any]) -> List[Any]
        """
        if not product_id:
            raise ValueError('Invalid ID')
        path = '/public/v1/products/' + product_id + '/parameters/' + parameter_id
        response = self._api.delete(
            path=path
        )
        return response

    def items(self, product_id):
        """Returns the ProductItemResource resource"""
        return ProductItemResource(self.config, 'products/{}'.format(product_id))
