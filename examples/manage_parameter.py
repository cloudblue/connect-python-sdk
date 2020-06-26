# -*- coding: utf-8 -*-

# This file is part of the Ingram Micro Cloud Blue Connect SDK.
# Copyright (c) 2019-2020 Ingram Micro. All Rights Reserved.
import json
from connect.config import Config
from connect.resources.product import ProductsResource


class Parameters():
    configuration = Config(file='examples/config.json')

    def list_parameters(self, product_id):
        product = ProductsResource(config=self.configuration)
        return product.list_parameters(product_id)

    def create_parameter(self, product_id, body):
        product = ProductsResource(config=self.configuration)
        return product.create_parameter(product_id, body)

    def update_parameter(self, product_id, parameter_id, body):
        product = ProductsResource(config=self.configuration)
        return product.update_parameter(product_id, parameter_id, body)

    def delete_parameter(self, product_id, param_id):
        product = ProductsResource(config=self.configuration)
        return product.delete_parameter(product_id, param_id)


def main():
    parameters_example = Parameters()
    with open('./tests/data/create_parameter_request.json') as json_file:
        body = json.load(json_file)
    parameters_example.create_parameter('PRD-075-401-854', body)


if __name__ == '__main__':
    main()
