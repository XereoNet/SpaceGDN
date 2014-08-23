import requests
import json
import datetime
import re
from ..resource_bases import ZipModifier


class Technic():

    listing_url = 'http://solder.technicpack.net/api/modpack'
    pack_url = 'http://solder.technicpack.net/api/modpack/%s'
    download_url = 'http://mirror.technicpack.net/Technic/servers/{name}/{cap_name}_Server_v{build}.zip'

    descriptions = {
        'release': 'An official release of a Minecraft version.',
        'snapshot': 'The latest testing snapshot of Minecraft. It may be unstable!'
    }

    def __init__(self):
        pass

    def load_pack(self, url, path, slug):
        modifier = ZipModifier()
        modifier.start_from_remote(url)
        modifier.patch_from_remote('http://s3.amazonaws.com/SpaceZips/forgepatch.zip')
        modifier.replace_in_file('config/forge.cfg', {
            'removeErroringEntities=false': 'removeErroringEntities=true',
            'removeErroringTileEntities=false': 'removeErroringTileEntities=true'
        })

        if slug == 'Hexxit':
            modifier.replace_in_file('config/InfernalMobs.cfg', {
                'useSimpleEntityClassnames=false': 'useSimpleEntityClassnames=true'
            })

        modifier.end_modify(path)

    def get_versions(self, slug):

        r = requests.get(self.pack_url % slug)
        data = json.loads(r.text)

        out = []
        for build in data['builds']:
            url = self.download_url.format(**{
                'name': data['name'],
                'cap_name': data['name'].capitalize(),
                'build': build
            })

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
                        'version': build
                    }
                ],
                '$id': build,
                '$load': lambda path, url=url, slug=slug: self.load_pack(url, path, slug),
                '$patched': True,
                'resource': 'build',
                'created': datetime.datetime.now(),
                'build': re.sub(r'[^0-9]', '', build),
                'url': url,
            })

        return out

    def get_packs(self):
        r = requests.get(self.listing_url)
        data = json.loads(r.text)

        if 'vanilla' in data['modpacks']:
            del data['modpacks']['vanilla']
        if 'hackslashmine' in data['modpacks']:
            del data['modpacks']['hackslashmine']

        return data['modpacks'].keys()

    def items(self):
        out = []
        for pack in self.get_packs():
            out.extend(self.get_versions(pack))

        return out