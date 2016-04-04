import requests
import urllib.parse
import re
import datetime
from gdn.log import logger

from bs4 import BeautifulSoup
from ..resource_bases import ForgePatcher


class CreeperRepo(ForgePatcher):

    base_url = 'http://www.creeperrepo.net/FTB2/'

    def parse_pack(self, elem):
        if not elem.has_attr('repoVersion'):
            return

        urlparts = {
            'dir': elem['dir'],
            'version': elem['repoVersion']
        }

        url = (self.base_url + urllib.parse.quote_plus('modpacks^{dir}^{version}'.format(**urlparts))
               + '/' + elem['url'])
        build = re.sub(r'[^0-9]', '', elem['version'])

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
                    'mc_version': elem['mcVersion'],
                    'last_build': build
                }
            ],
            '$id': elem['version'],
            '$load': lambda path: self.patch_download(elem['mcVersion'], url, path),
            '$patched': True,
            'resource': 'build',
            'created': datetime.datetime.now(),
            'build': build,
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
