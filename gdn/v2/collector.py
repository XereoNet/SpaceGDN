from ..app import app
from .strategies import strategies


class Collector():

    def __init__(self):
        self.result = {}
        self.page = 1
        self.request = None
        self.pointer = None

        self.pagination_data = {
            'limit': app.config['PAGE_LENGTH'],
            'page': 1,
            'count': 0
        }

    def collect(self, request, path):
        self.request = request

        s = self.request.args.get('strategy')
        if not s in strategies:
            s = 'find'

        strategy_instance = strategies[s](self.request, path)
        self.pointer = strategy_instance.results(self.set_page)

    def results(self):
        if not 'results' in self.result:
            self.result['results'] = self.pointer
            self.result['pagination'] = self.pagination()

        return self.result

    def set_page(self, pointer):
        self.pointer = pointer

        self.pagination_data['count'] = pointer.count()
        self.pointer.limit(app.config['PAGE_LENGTH'])

        if 'page' in self.request.args:
            self.pagination_data['page'] = max(int(self.request.args.get('page')), 1)
            self.pagination_data['limit'] = (self.page - 1) * app.config['PAGE_LENGTH']

            self.pointer.skip(self.pagination_data['limit'])

        return self.pointer

    def pagination(self):
        return {
            'page':  self.pagination_data['page'],
            'items':  self.pagination_data['count'],
            'per_page':  self.pagination_data['limit'],
            'has_next':  self.pagination_data['limit'] ==  self.pagination_data['count'],
            'has_prev': self.pagination_data['page'] > 1
        }