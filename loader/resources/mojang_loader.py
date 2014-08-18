import requests
import json
import datetime
import re
import math
from ..resource_bases import Downloader


class Mojang(Downloader):

    url = 'http://s3.amazonaws.com/Minecraft.Download/versions/versions.json'
    download_url_base = 'https://s3.amazonaws.com/Minecraft.Download/versions/{0}/minecraft_server.{0}.jar'

    descriptions = {
        'release': 'An official release of a Minecraft version.',
        'snapshot': 'The latest testing snapshot of Minecraft. It may be unstable!'
    }

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
                    '$id': version['type'],
                    'resource': 'type',
                    'name': ' '.join([n.capitalize() for n in version['type'].split('_')]),
                    'author': 'Mojang',
                    'description': self.get_description(version['type'])
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