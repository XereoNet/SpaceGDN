from ..mongo import db
from ..app import app
import pymongo

class Collector():

    operators = ['$gt', '$gte', '$in', '$lt', '$lte', '$ne', '$nin', '$eq']
    arrayOperators = ['$nin', '$in']

    def __init__(self):
        self.result = {}
        self.page = 1
        self.find = {'limit': app.config['PAGE_LENGTH']}

    def _collect_route(self, route):
        parts = route.strip('/').split('/')
        if len(parts) == 0:
            return

        self.find.setdefault('spec', {})['parents'] = parts.pop()

    def _collect_r(self, resource):
        self.find.setdefault('spec', {})['resource'] = resource

    def _collect_sort(self, sorting):
        for sort in sorting.split('|'):
            data = sort.split('.', 1)

            if len(data)!= 2:
                continue

            data[1] = pymongo.ASCENDING if data[1] == 'asc' else pymongo.DESCENDING

            self.find.setdefault('sort', []).append(tuple(data))

    def _collect_where(self, wheres):
        for where in wheres.split('|'):
            data = where.split('.', 2)

            if len(data) != 3:
                continue

            key, operator, value = data

            if not operator in self.operators:
                continue

            if operator in self.arrayOperators:
                value = value.split(',')

            if operator == '$eq':
                self.find.setdefault('spec', {})[key] = value
            else:
                self.find.setdefault('spec', {})[key] = {operator: value}

    def _collect_page(self, page):
        self.page = max(int(page), 1)
        self.find['skip'] = (self.page - 1) * app.config['PAGE_LENGTH']

    def collect(self, route, params):
        self.params = params
        self.params['route'] = route

        for collector in ['route', 'r', 'sort', 'where', 'page']:
            if collector in self.params:
                getattr(self, '_collect_' + collector)(self.params[collector])

    def results(self):
        if not 'results' in self.result:
            print(self.find)
            self.result['results'] = [dict(result) for result in db.items.find(**self.find)]
            self.result['pagination'] = self.pagination()

        return self.result

    def pagination(self):
        return {
            'page': self.page,
            'per_page': app.config['PAGE_LENGTH'],
            'has_next': app.config['PAGE_LENGTH'] == len(self.result['results']),
            'has_prev': self.page > 1
        }