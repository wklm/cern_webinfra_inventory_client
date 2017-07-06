import os
from io import BytesIO

import requests
from rest_framework.parsers import JSONParser

from property import Property


class Inventory:
    def __init__(self):
        self.api_root = os.environ['INVENTORY_ADDRESS']
        self.endpoints = [endpoint
                          for endpoint in requests.get(self.api_root).json()]

        self.model_names = {model_name.split('/')[2]: model_name
                            for model_name in self.endpoints}

    def add_instance(self, instance_type, properties):

        try:
            model_name = self.model_names[instance_type]
            Model(model_name).validate(properties)

            resp = requests.post(self.api_root + '/' + model_name + '/', properties)

            print(resp.content)

        except KeyError:
            raise Exception(
                'No model named %s. Available model names: %s'
                % (instance_type, [name for name in self.model_names.keys()])
            )

    @staticmethod
    def get_instance_fields(instance_name):
        return Model(instance_name).fields

    def get_instances(self, instance_type):
        pass

    @staticmethod
    def deserialize_property(property):
        return property


class Model:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.schema = BytesIO(
            requests.options(
                Inventory().api_root + '/' + self.endpoint + '/?format=json'
            ).content
        )
        self.fields = dict(JSONParser().parse(self.schema)['actions']['POST'])

    def validate(self, properties):
        key_diff = (self.fields.keys() - properties.keys() or
                    properties.keys() - self.fields.keys())
        if key_diff:
            raise Exception(
                'provided fields don\'t match the model %s. %s are missing'
                % (self.endpoint, key_diff)
            )
        for key in self.fields:
            validating_schema = Property(self.fields[key])
            provided_value = properties[key]

            if type(provided_value) is not validating_schema.type:
                raise Exception(
                    '{0}: {1} is a {2}, but should be: {3}'.format(
                        key,
                        provided_value,
                        type(provided_value),
                        validating_schema.type
                    )
                )
