import requests
import urllib.parse
import re
import datetime
from gdn.log import logger

from bs4 import BeautifulSoup
from ..resource_bases import ZipModifier


class CreeperRepo():

    base_url = 'http://www.creeperrepo.net/FTB2/'

    def load_pack(self, elem, url, path):
        md5sum = None
        r = requests.get(url + '.md5')
        if r.status_code == requests.codes.ok:
            md5sum = r.text.strip()

        modifier = ZipModifier()
        modifier.start_from_remote(url, md5sum=md5sum)
        modifier.patch_from_remote('http://s3.amazonaws.com/SpaceZips/forgepatch.zip')
        modifier.replace_in_file('config/forge.cfg', {
            'removeErroringEntities=false': 'removeErroringEntities=true',
            'removeErroringTileEntities=false': 'removeErroringTileEntities=true'
        })

        if elem['name'] == 'Agrarian Skies: Hardcore Quest':
            modifier.ensure_dir_present('lib')
            modifier.ensure_dir_present('libraries')

        modifier.end_modify(path)

    def parse_pack(self, elem):
        if not elem.has_attr('repoVersion'):
            return

        urlparts = {
            'dir': elem['dir'],
            'version': re.sub('\.', '_', elem['repoVersion'])
        }

        url = (self.base_url + urllib.parse.quote_plus('modpacks^{dir}^{version}'.format(**urlparts))
               + '/' + elem['url'])

        return {
            '$parents': [
                {
                    '$id': 'minecraft',
                    'resource': 'game',
                    'name': 'Minecraft'
                }, {
                    '$id': elem['name'],
                    'resource': 'type',
                    'name': elem['name'],
                    'author': elem['author'],
                    'description': elem['description']
                }, {
                    '$id': elem['version'],
                    'resource': 'version',
                    'version': elem['version'],
                    'mc_version': elem['mcVersion']
                }
            ],
            '$id': elem['version'],
            '$load': lambda path: self.load_pack(elem, url, path),
            '$patched': True,
            'resource': 'build',
            'created': datetime.datetime.now(),
            'build': re.sub(r'[^0-9]', '', elem['version']),
            'url': url,
        }

    def get_xml(self):
        out = []

        for url in ([
            'http://new.creeperrepo.net/FTB2/static/thirdparty.xml',
            'http://www.creeperrepo.net/FTB2/static/modpacks.xml'
        ]):
            r = requests.get(url)
            d = BeautifulSoup(r.content, 'xml')

            out.extend(d.find_all('modpack'))

        return out

    def items(self):
        return map(self.parse_pack, self.get_xml())