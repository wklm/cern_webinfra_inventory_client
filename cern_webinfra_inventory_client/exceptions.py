class UnmatchedPropertyType(Exception):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return 'Following Models are missing:', self.type


class ModelNotFound(Exception):
    def __init__(self, model, model_names):
        self.model = model
        self.model_names = model_names

    def __str__(self):
        return 'No model named {0}. Available model names: {1}' \
            .format(self.model, [name for name in self.model_names.keys()])


class MissingProperties(Exception):
    def __init__(self, endpoint, key_diff):
        self.endpoint = endpoint
        self.key_diff = key_diff

    def __str__(self):
        return 'provided fields don\'t match the model {0}. {1} is missing' \
            .format(self.endpoint, self.key_diff)


class UnknownProperty(Exception):
    def __init__(self, key, endpoint):
        self.endpoint = endpoint
        self.key = key

    def __str__(self):
        return 'invalid property {0} for endpoint {1}'.format(
            self.key, self.endpoint
        )


class InvalidPropertyType(Exception):
    def __init__(self, key, provided_value, validating_schema):
        self.key = key
        self.provided_value = provided_value
        self.validating_schema = validating_schema


    def __str__(self):
        return '{0}: {1} is a {2}, but should be: {3}'.format(
            self.key,
            str(self.provided_value),
            type(self.provided_value),
            self.validating_schema.type
        )
