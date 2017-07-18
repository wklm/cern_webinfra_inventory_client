import datetime
from exceptions import UnmatchedPropertyType


class Property:  # TODO: !!! PROPER DESERIALIZATION WITH A TYPE SYSTEM !!!
    
    TYPES_MAPPING = {
        'integer':  int,
        'string':   str,
        'boolean':  bool,
        'date':     datetime.date,
        'datetime': datetime.datetime,
        'choice':   str,
    }
    
    def __init__(self, spec):
        self.spec = spec
        self.type = self.TYPES_MAPPING.get(spec['type'], None)
        if not self.type: raise UnmatchedPropertyType(t)

        self.required = bool(spec['required'])
        self.read_only = bool(spec['read_only'])
        self.label = str(spec['label'])
        if type(self.type) is int:
            self.min_value = int(spec['min_value'])
            self.min_value = int(spec['max_value'])
        elif type(self.type) is str:
            self.max_length = spec['max_length']
            
    def __str__(self):
        return str(self.spec)
