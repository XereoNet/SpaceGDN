class loader_json:

    def __init__(self):
        pass

    def load(self, data, _):
        return data['releases']
