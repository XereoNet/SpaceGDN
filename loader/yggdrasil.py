import hashlib
import os
import requests
from gdn.mongo import db


class Yggdrasil():

    def __init__(self, config):
        self.config = config
        self.id_cache = {}

    def has_id(self, id):
        if not id in self.id_cache:
            result = db.items.find_one({'_id': id})
            self.id_cache[id] = False if result is None else True

        return self.id_cache[id]

    def create_id(self, idlist):
        iid = hashlib.md5()

        for i in idlist:
            iid.update(i.encode('utf-8'))

        return iid.hexdigest()

    def make_parents(self, parents):
        ids = []
        hashed_ids = []
        for parent in parents:
            ids.append(parent['$id'])
            pid = self.create_id(ids)
            hashed_ids.append(pid)

            if self.has_id(pid):
                continue

            data = self.strip_metas(parent)
            data['_id'] = pid

            if hashed_ids:
                data['parents'] = hashed_ids

            self.id_cache[pid] = True
            db.items.insert(data)

        return hashed_ids

    def strip_metas(self, obj):
        out = {}
        for key, value in obj.items():
            if not key.startswith('$'):
                out[key] = value

        return out

    def md5sum(self, path='', remote=''):
        md5 = hashlib.md5()

        if path == '':
            r = requests.get(remote, stream=True)
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    md5.update(chunk)
        else:
            with open(path, 'rb') as f:
                while True:
                    data = f.read(2**20)
                    if not data:
                        break
                    md5.update(data)

        return md5.hexdigest()

    def make_item(self, item):
        idlist = [p['$id'] for p in item['$parents']]
        idlist.append(item['$id'])
        iid = self.create_id(idlist)

        if self.has_id(iid):
            return

        data = self.strip_metas(item)
        data['_id'] = iid

        if ('$load' in item and self.config['CACHE_ALWAYS']) or \
                (self.config['CACHE_PATCHED'] and '$patched' in item and item['$patched']):
            path, url = self.resolve_filename(data)
            item['$load'](path)
            data['url'] = url
            data['md5'] = self.md5sum(path=path)
        else:
            data['md5'] = self.md5sum(remote=data['url'])

        data['parents'] = self.make_parents(item['$parents'])

        self.id_cache[iid] = True
        db.items.insert(data)

    def resolve_filename(self, data):
        part = 'static/cache/%s.%s' % (data['_id'], data['url'].split('.').pop())

        url = 'http://%s:%s/%s' % (self.config['HTTP_HOST'], self.config['HTTP_PORT'], part)
        path = os.path.join(os.path.dirname(__file__), '../gdn', part)

        return path, url

    def run(self, loaders):
        for loader in loaders:
            for item in loader.items():
                self.make_item(item)