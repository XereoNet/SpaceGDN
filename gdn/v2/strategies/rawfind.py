from ...mongo import db
from ..requestException import RequestException

class RawFind:

    def __init__(self, request, path):
        self.data = request.json['find']

    def results(self, pointer_func):
        try:
            return [dict(result) for result in db.items.find(self.data)]
        except Exception as e:
            raise RequestException(*e.args)