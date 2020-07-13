# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.

from requests import RequestException

from .base import BaseResource
from connect.exceptions import DeleteResourceError, ServerError, UpdateResourceError
from ..models import Marketplace


class MarketplaceResource(BaseResource):
    """ Resource to work with :py:class:`connect.models.Marketplace` models.
        :param Config config: Config object or ``None`` to use environment config (default).
    """
    DELETE_ERR = 'Error deleting marketplace {}: {}'
    UPLOAD_ERR = 'Error uploading icon for Marketplace {}: {}'
    RESPONSE_ERR = 'Unexpected server response, returned code {} -- Raw response: {}'
    resource = 'marketplaces'
    model_class = Marketplace

    def __init__(self, config=None):
        super(MarketplaceResource, self).__init__(config)

    def set_icon(self, id_, path):
        """ Sets or updates the Marketplace icon.

        :param str id_: Id of the Marketplace.
        :param str path: Path to the icon file that will be sent to Connect.
        :return: Whether the icon was successfully uploaded.
        :rtype: bool
        """
        icon = self._load_icon(id_, path)
        request_path, headers, multipart = self._setup_icon_request(id_, path, icon)
        self._post_icon_request(id_, request_path, headers, multipart)

    def _load_icon(self, id_, path):
        # type: (str, str) -> bytes
        try:
            with open(path, 'rb') as f:
                return f.read()
        except IOError as ex:
            raise UpdateResourceError(self.UPLOAD_ERR.format(id_, ex))

    def _setup_icon_request(self, id_, path, icon):
        # type: (str, str, bytes) -> (str, dict, dict)
        request_path = self._api.urljoin(id_, 'icon')
        headers = self._api.headers
        headers['Accept'] = 'application/json'
        del headers['Content-Type']  # This must NOT be set for multipart post requests
        multipart = {'icon': (path, icon)}
        self.logger.info('HTTP Request: {} - {} - {}'.format(request_path, headers, multipart))
        return request_path, headers, multipart

    def _post_icon_request(self, id_, path, headers, multipart):
        # type: (str, str, dict, dict) -> None
        try:
            content, status = self._api.post(
                path=path,
                headers=headers,
                files=multipart)
        except (RequestException, ServerError) as ex:
            raise UpdateResourceError(self.UPLOAD_ERR.format(id_, ex))
        self._raise_if_invalid_status(200, status, content, UpdateResourceError)

    def _raise_if_invalid_status(self, required, obtained, content, ex_class):
        # type: (int, int, str, type) -> None
        self.logger.info('HTTP Code: {}'.format(obtained))
        if obtained != required:
            msg = self.RESPONSE_ERR.format(obtained, content)
            self.logger.error(msg)
            raise ex_class(msg)

    def delete(self, id_):
        """ Deletes a Marketplace.

        :param id_: Id of the Marketplace.
        :return:
        """
        try:
            content, status = self._api.delete(path=id_)
        except (RequestException, ServerError) as ex:
            raise DeleteResourceError(self.DELETE_ERR.format(id_, ex))
        self._raise_if_invalid_status(204, status, content, DeleteResourceError)
