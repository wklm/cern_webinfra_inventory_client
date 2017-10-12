import os
from io import BytesIO

import requests
from django.conf import settings

settings.configure()
from rest_framework.parsers import JSONParser
from .property import Property
from .exceptions import ModelNotFound, MissingProperties, \
    InvalidPropertyType, EntryAlreadyExists, InternalInventoryError, \
    UnknownProperty


class Inventory:
    def __init__(self):
        self.api_root = os.environ['INVENTORY_URL']
        self.endpoints = [
            endpoint for endpoint in requests.get(self.api_root).json()
        ]
        self.model_names = {
            str(model_name.split('/')[2]): model_name
            for model_name in self.endpoints
        }

    def add_instance(self, instance_type, properties):
        if not self._get_entry(properties['name'], instance_type):
            model = self._get_model(instance_type, properties)
            return requests.post(
                self.api_root + '/' + model.endpoint + '/', properties
            )
        raise EntryAlreadyExists(instance_type, properties)

    def edit_instance(self, instance_type, instance_name, edited_prop, value):
        model = self._get_model(instance_type)
        if edited_prop not in model.fields:
            raise UnknownProperty(edited_prop, model.endpoint)
        entry = self._get_entry(instance_name, instance_type)
        entry[edited_prop] = value
        model.validate(entry)
        return requests.put(
            self.api_root + '/' + model.endpoint + '/', entry
        )

    def delete_instance(self, name):
        return requests.delete(
            self.api_root + '/rest/namespace/instance/?name=' + name
        )

    def _get_model(self, instance_type, properties=None):
        try:
            model = Model(self.model_names[instance_type])
            if properties:
                model.validate(properties)
            return model
        except KeyError:
            raise ModelNotFound(instance_type, self.model_names)

    def _get_entry(self, instance_name, instance_type='instance'):
        entries = self.get_instance(instance_type)
        for site in entries.json():
            if site['name'] == instance_name:
                return site

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
