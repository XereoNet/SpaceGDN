from ...mongo import db
from ..requestException import RequestException

class Aggregate:

    def __init__(self, request, path):
        self.data = request.json['aggregation']

    def results(self, pointer_func):
        try:
            return db.items.aggregate(self.data)['result']
        except Exception as e:
            raise RequestException(*e.args)