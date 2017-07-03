import requests
import os
import json

from django.conf import settings

settings.configure()
from io import StringIO, BytesIO
from rest_framework.parsers import JSONParser
from rest_framework import serializers


class Inventory:
    def __init__(self):
        self.api_root = 'http://localhost:8080' # os.environ['INVENTORY_ADDRESS']
        self.endpoints = [endpoint for endpoint in requests.get(self.api_root).json()]

    def add_instance(self, instance_type, properties):
        model_names = {model_name.split('/')[2]: model_name for model_name in self.endpoints}

        if not model_names[instance_type]:
            raise Exception('No model named %s. \n\t Available model names: %s' % (type, model_names))

        print(Model(model_names[instance_type]).fields)




class Model:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @property
    def schema(self):
        return BytesIO(
            requests.options(
                Inventory().api_root + '/' + self.endpoint + '/?format=json'
            ).content
        )

    @property
    def fields(self):
        return dict(JSONParser().parse(self.schema)['actions']['POST'])





Inventory().add_instance("sharepoint", {})

import pdb
pdb.set_trace()
