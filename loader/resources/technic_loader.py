import requests
import json
import datetime
import re
from ..resource_bases import Downloader


class Technic(Downloader):

    api_url = 'http://solder.technicpack.net/api/modpack/'
    download_url = 'http://mirror.technicpack.net/Technic/servers/'

    mapping = {
            'attack-of-the-bteam': 'bteam/BTeam_Server_v',
            'hexxit': 'hexxit/Hexxit_Server_v',
            'blightfall': 'blightfall/Blightfall_Server_v',
            'tekkit-legends': 'tekkit-legends/Tekkit_Legends_Server_v',
            'bigdig': 'bigdig/BigDigServer_v',
            'tekkitmain': 'tekkitmain/Tekkit_Server_v',
            'tekkit': 'tekkit/Tekkit_Server_',
            'tekkitlite': 'tekkitlite/Tekkit_Lite_Server_',
            'voltz': 'voltz/Voltz_Server_v'
        }

    def get_versions(self, slug):
        out = []

        r = requests.get(self.api_url + slug)
        if not r.ok:
            return out
        data = r.json()

        download_name = self.mapping[data['name']]

        for build in data['builds']:
            url = self.download_url + download_name + build + '.zip'

            build_num = re.sub(r'[^0-9]', '', build)

            out.append({
                '$parents': [
                    {
                        '$id': 'minecraft',
                        'resource': 'game',
                        'name': 'Minecraft'
                    }, {
                        '$id': slug,
                        'resource': 'type',
                        'name': data['display_name'],
                        'author': 'TechnicPack',
                        'description': ''
                    }, {
                        '$id': build,
                        'resource': 'version',
                        'version': build,
                        'last_build': build_num
                    }
                ],
                '$id': build,
                '$load': lambda path: self.download(url, path),
                'resource': 'build',
                'created': datetime.datetime.now(),
                'build': build_num,
                'url': url,
            })

        return out

    def items(self):
        out = []
        for pack in self.mapping.keys():
            out.extend(self.get_versions(pack))

        return out
