import datetime
from cern_webinfra_inventory_client.exceptions import UnmatchedPropertyType


class Property:  # TODO: !!! PROPER DESERIALIZATION WITH A TYPE SYSTEM !!!
    def __init__(self, spec):
        self.spec = spec
        self.type = self._get_type(spec['type'])
        self.required = bool(spec['required'])
        self.read_only = bool(spec['read_only'])
        self.label = str(spec['label'])
        if type(self.type) is int:
            self.min_value = int(spec['min_value'])
            self.min_value = int(spec['max_value'])
        elif type(self.type) is str:
            self.max_length = spec['max_length']

    @staticmethod
    def _get_type(t):
        if t == 'integer':  return int
        if t == 'string':   return str
        if t == 'boolean':  return bool
        if t == 'date':     return datetime.date
        if t == 'datetime': return datetime.datetime
        if t == 'choice':   return str
        raise UnmatchedPropertyType(t)

    def __str__(self):
        return str(self.spec)
