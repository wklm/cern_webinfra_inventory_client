from io import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework import serializers


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