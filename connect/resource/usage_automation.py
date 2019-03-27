# -*- coding: utf-8 -*-

"""
This file is part of the Ingram Micro Cloud Blue Connect SDK.
Copyright (c) 2019 Ingram Micro. All Rights Reserved.
"""
from abc import ABCMeta

import openpyxl
import requests
from openpyxl.writer.excel import save_virtual_workbook
from typing import Dict, Any, List

from connect.logger import logger
from connect.models.exception import FileCreationError
from connect.models.product import Product
from connect.models.usage import FileSchema, Listing, File, FileUsageRecord
from connect.resource import AutomationResource


class UsageAutomation(AutomationResource):
    __metaclass__ = ABCMeta
    resource = 'usage/files'
    schema = FileSchema(many=False)

    def build_filter(self, status='listed'):
        # type: (str) -> Dict[str, Any]
        filters = super(UsageAutomation, self).build_filter(status)
        if self.config.products:
            filters['product__id'] = ','.join(self.config.products)
        return filters

    def dispatch(self, request):
        # type: (Listing) -> str

        if self.config.products \
                and request.product.id not in self.config.products:
            return 'Listing not handled by this processor'

        logger.info(
            'Processing Usage for Product {} ({}) '.format(request.product.id,
                                                           request.product.name) +
            'on Contract {} '.format(request.contract.id) +
            'and provider {}({})'.format(request.provider.id, request.provider.name))

        try:
            result = self.process_request(request)
        except FileCreationError:
            logger.info(
                'Error processing Usage for Product {} ({}) '.format(request.product.id,
                                                                     request.product.name) +
                'on Contract {} '.format(request.contract.id) +
                'and provider {}({})'.format(request.provider.id, request.provider.name))
            return 'failure'

        logger.info('Processing result for usage on listing {}: {}'
                    .format(request.product.id, result))
        return 'success'

    def create_usage_file(self, usage_file):
        # type: (File) -> File
        if not usage_file.name or not usage_file.product.id or not usage_file.contract.id:
            raise FileCreationError('Usage File Creation requires name, product id, contract id')
        if not usage_file.description:
            # Could be because description is empty or None, so make sure it is empty
            usage_file.description = ''
        response = self.api.post(self._list_url, data=usage_file)
        return self._load_schema(response)

    @staticmethod
    def create_usage_spreadsheet():
        # type: () -> openpyxl.Workbook
        book = openpyxl.Workbook()
        sheet = book.active
        sheet.title = 'usage_records'
        sheet['A1'] = 'usage_record_id'
        sheet['B1'] = 'item_search_criteria'
        sheet['C1'] = 'item_search_value'
        sheet['D1'] = 'quantity'
        sheet['E1'] = 'start_time_utc'
        sheet['F1'] = 'end_time_utc'
        sheet['G1'] = 'asset_search_criteria'
        sheet['H1'] = 'asset_search_value'
        return book

    def upload_spreadsheet(self, usage_file, spreadsheet):
        # type: (File, openpyxl.Workbook) -> None

        # Generate spreadsheet file
        file_contents = save_virtual_workbook(spreadsheet)

        # Setup request
        url = self._obj_url(usage_file.id, 'upload/')
        headers = self.api.headers
        headers['Accept'] = 'application/json'
        delattr(headers, 'Content-Type')  # This must NOT be set for multipart post requests
        multipart = {'usage_file': ('usage_file.xlsx', file_contents)}
        logger.info('HTTP Request: {} - {} - {}'.format(url, headers, multipart))

        # Post request
        try:
            response = requests.post(url, headers=headers, files=multipart)
        except requests.RequestException as ex:
            raise FileCreationError('Error uploading file: {}'.format(ex))
        logger.info('HTTP Code: {}'.format(response.status_code))
        if response.status_code != 201:
            msg = 'Unexpected server response, returned code {}'.format(response.status_code)
            logger.error('{} -- Raw response: {}'.format(msg, response.content))
            raise FileCreationError(msg)

    def create_populated_spreadsheet(self, file_usage_records):
        # type: (List[FileUsageRecord]) -> openpyxl.Workbook
        book = self.create_usage_spreadsheet()
        sheet = book.active
        for index, record in enumerate(file_usage_records):
            row = str(index + 2)
            sheet['A' + row] = record.id
            sheet['B' + row] = record.item_search_criteria
            sheet['C' + row] = record.item_search_value
            sheet['D' + row] = record.quantity
            sheet['E' + row] = record.start_time_utc
            sheet['F' + row] = record.end_time_utc
            sheet['G' + row] = record.asset_search_criteria
            sheet['H' + row] = record.asset_search_value
        return book

    def upload_usage_records(self, usage_file, file_usage_records):
        # type: (File, List[FileUsageRecord]) -> None
        # TODO: Using xslx mechanism till usage records json api is available
        book = self.create_populated_spreadsheet(file_usage_records)
        self.upload_spreadsheet(usage_file, book)

    """
    def get_usage_template_file(self, product):
        # type: (Product) -> str
        response = self.api.get(self._obj_url())
        response = self.api.check_response(requests.get(ur, headers=self.api.headers))
        return self.check_response(response)
    """
