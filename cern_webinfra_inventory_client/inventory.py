class Inventory:
    def __init__(self):
        self.api_root = os.environ['INVENTORY_ADDRESS']
        self.endpoints = [endpoint for endpoint in requests.get(self.api_root).json()]

    def add_instance(self, instance_type, properties):
        model_names = {model_name.split('/')[2]: model_name for model_name in self.endpoints}

        if not model_names[instance_type]:
            raise Exception('No model named %s. \n\t Available model names: %s' % (type, model_names))

        return Model(model_names[instance_type]).fields

    def deserialize_property(self, property):
        return property


