from ...mongo import db
import re
import pymongo


class Find:

    operators = ['$gt', '$gte', '$in', '$lt', '$lte', '$ne', '$nin', '$eq']
    arrayOperators = ['$nin', '$in']

    def __init__(self, request, path):
        self.parents = False
        self.find = {}

        params = request.args.to_dict()
        params['route'] = path

        for collector in ['route', 'r', 'sort', 'where', 'page', 'parents']:
            if collector in params:
                getattr(self, '_collect_' + collector)(params[collector])

    def _collect_route(self, route):
            parts = route.strip('/').split('/')
            if len(parts) == 0 or parts == ['']:
                return

            parent = parts.pop()

            if len(parent) == 32:
                self.find.setdefault('spec', {})['parents'] = parent
            elif parent.isalnum():
                self.find.setdefault('spec', {})['parents'] = re.compile('^' + parent, re.IGNORECASE)

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

    def _collect_parents(self, parents):
        self.parents = True
        self.find['limit'] = 10

    def results(self, pointer_func):
        items = [dict(result) for result in pointer_func(db.items.find(**self.find))]

        if self.parents:
            for item in items:
                parents = item['parents']
                item['parents'] = []
                for parent in parents:
                    r = db.items.find_one({'_id': parent})
                    del r['parents']

                    item['parents'].append(r)

        return items