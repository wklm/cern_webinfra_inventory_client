import os
from io import BytesIO
import requests
from django.conf import settings

settings.configure()
from rest_framework.parsers import JSONParser
from property import Property
from exceptions import ModelNotFound, MissingProperties, InvalidPropertyType


class Inventory:
    def __init__(self):
        self.api_root = os.environ['INVENTORY_ADDRESS']
        self.endpoints = [
            endpoint for endpoint in requests.get(self.api_root).json()
        ]
        self.model_names = {
            str(model_name.split('/')[2]): model_name
            for model_name in self.endpoints
        }

    def add_instance(self, instance_type, properties):
        try:
            model_name = self.model_names[instance_type]
            Model(model_name).validate(properties)
            return requests.post(
                self.api_root + '/' + model_name + '/', properties
            )
        except KeyError:
            raise ModelNotFound(instance_type, self.model_names)

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
        for key in self.fields:
            if key not in properties and not self._is_nullable(key):
                raise MissingProperties(self.endpoint, key)

            validating_schema = Property(self.fields[key])
            provided_value = properties[key]

            if type(provided_value) is not validating_schema.type:
                raise InvalidPropertyType(
                    key,
                    provided_value,
                    validating_schema
                )

    def _is_nullable(self, key):
        if self.fields[key]['required']:
            return False
        return True
