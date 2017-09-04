import os
from io import BytesIO

import requests
from django.conf import settings

settings.configure()
from rest_framework.parsers import JSONParser
from .property import Property
from .exceptions import ModelNotFound, MissingProperties, \
    InvalidPropertyType, EntryAlreadyExists, InternalInventoryError


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
        if self._entry_exists(instance_type, properties):
            raise EntryAlreadyExists(instance_type, properties)
        try:
            model_name = self.model_names[instance_type]
            Model(model_name).validate(properties)
            return requests.post(
                self.api_root + '/' + model_name + '/', properties
            )
        except KeyError:
            raise ModelNotFound(instance_type, self.model_names)

    def edit_instance(self, name, properties):
        raise NotImplementedError

    def delete_instance(self, name):
        raise NotImplementedError

    def _entry_exists(self, instance_type, properties):
        entries = self.get_instance(instance_type)
        for site in entries.json():
            if site['name'] == properties['name']:
                return True
        return False

    @staticmethod
    def get_instance_fields(instance_name):
        return Model(instance_name).fields

    def get_instance(self, instance_type):
        resp = requests.get(
            self.api_root + '/rest/namespace/' + instance_type
        )
        if resp.status_code == 200:
            return resp
        if resp.status_code == 404:
            raise ModelNotFound(instance_type, self.model_names)
        if resp.status_code == 500:
            raise InternalInventoryError()


class Model:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.schema = BytesIO(
            requests.options(
                Inventory().api_root + '/' + self.endpoint + '/?format=json'
            ).content
        )
        self.fields = dict(
            JSONParser()
                .parse(self.schema)['actions']['POST']
        )

    def validate(self, properties):
        for key in self.fields:
            if key not in properties and not self._is_nullable(key):
                raise MissingProperties(self.endpoint, key)

            validating_schema = Property(self.fields[key])
            try:  # TODO: ...
                provided_value = properties[key]
            except KeyError:
                continue

            if type(provided_value) is not validating_schema.type:
                raise InvalidPropertyType(
                    key,
                    provided_value,
                    validating_schema
                )

    def _is_nullable(self, key):
        return not self.fields[key]['required']
