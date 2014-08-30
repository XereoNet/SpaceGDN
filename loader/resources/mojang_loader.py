import requests
import json
import datetime
import re
import math
from ..resource_bases import Downloader


class Mojang(Downloader):

    url = 'http://s3.amazonaws.com/Minecraft.Download/versions/versions.json'
    download_url_base = 'https://s3.amazonaws.com/Minecraft.Download/versions/{0}/minecraft_server.{0}.jar'

    def __init__(self):
        pass

    def load_pack(self, path, url):
        r = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    def get_description(self, t):
        if t in self.descriptions:
            return self.descriptions[t]

        return ''

    def parse_version(self, version):

        if version['type'].startswith('old_'):
            return

        url = self.download_url_base.format(version['id'])
        released = datetime.datetime.strptime(re.sub(r'\+[0-9]{2}:[0-9]{2}$', '',
                                                     version['releaseTime']), '%Y-%m-%dT%H:%M:%S')
        return {
            '$parents': [
                {
                    '$id': 'minecraft',
                    'resource': 'game',
                    'name': 'Minecraft'
                }, {
                    '$id': 'vanilla',
                    'resource': 'type',
                    'name': 'Vanilla Minecraft',
                    'author': 'Mojang',
                    'description': ''
                }, {
                    '$id': version['type'],
                    'resource': 'channel',
                    'name': ' '.join([n.capitalize() for n in version['type'].split('_')])
                }, {
                    '$id': version['id'],
                    'resource': 'version',
                    'version': version['id']
                }
            ],
            '$id': version['id'],
            '$load': lambda path: self.download(url, path),
            '$patched': False,
            'resource': 'build',
            'created': released,
            'build': math.floor(released.timestamp() / 100),
            'url': url,
        }

    def get_versions(self):
        r = requests.get(self.url)
        data = json.loads(r.text)

        return data['versions']

    def items(self):
        return map(self.parse_version, self.get_versions())