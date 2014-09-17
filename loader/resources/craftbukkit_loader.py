import requests
import json
import re
import datetime
from ..resource_bases import Downloader


class CraftBukkit(Downloader):

    base_url = 'http://dl.bukkit.org'

    def __init__(self):
        pass

    def parse_results(self, result):

        if result['is_broken']:
            return

        return {
            '$parents': [
                {
                    '$id': 'minecraft',
                    'resource': 'game',
                    'name': 'Minecraft'
                }, {
                    '$id': 'craftbukkit',
                    'resource': 'type',
                    'name': 'CraftBukkit',
                    'author': 'Bukkit',
                    'description': ''
                }, {
                    '$id': result['channel']['slug'],
                    'resource': 'channel',
                    'name': result['channel']['name']
                }, {
                    '$id': result['version'],
                    'resource': 'version',
                    'version': result['version'],
                    'mc_version': re.search(r'^[0-9\.]+', result['version']).group(0),
                    'last_build': result['build_number']
                }
            ],
            '$id': str(result['build_number']),
            '$load': lambda path: self.download(result['file']['url'], path, result['file']['checksum_md5']),
            '$patched': False,
            'resource': 'build',
            'created': datetime.datetime.strptime(result['created'], '%Y-%m-%d %H:%M:%SZ'),
            'build': result['build_number'],
            'url': result['file']['url'],
        }

    def get_json(self):
        out = []
        for channel in ['dev', 'beta', 'rb']:
            r = requests.get('http://dl.bukkit.org/api/1.0/downloads/projects/craftbukkit/artifacts/' + channel)
            data = json.loads(r.text)

            out.extend(data['results'])

        return out

    def items(self):
        return map(self.parse_results, self.get_json())