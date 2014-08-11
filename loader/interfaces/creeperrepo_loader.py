import requests
import urllib
import re
from lxml import etree as ET


class loader_creeperrepo:

    base_url = 'http://www.creeperrepo.net'

    def __init__(self):
        pass

    def artifactURLs(self):
        return [
            'http://new.creeperrepo.net/FTB2/static/thirdparty.xml',
            'http://www.creeperrepo.net/FTB2/static/modpacks.xml'
        ]

    def getData(self, name, version, file_):

        url = (self.base_url + '/FTB2/' +
               urllib.quote_plus('modpacks^{}^{}^{}'.format(name, version,
                                                            file_)))

        # site = requests.head(url)

        # size = site.headers['content-length'];

        return url

    def getXML(self, name):
        for url in self.artifactURLs():
            r = requests.get(url)
            d = ET.fromstring(r.content).find('modpack[@name="{}"]'.format(
                name))

            if d is not None:
                return d

    def load(self, channel, last_build):
        modpack = self.getXML(channel['full_name'])

        build = int(re.sub('[^0-9]', '', modpack.get('repoVersion')))
        if build == last_build:
            return []

        url = self.getData(modpack.get('dir'),
                           re.sub('\\.', '_', modpack.get('repoVersion')),
                           modpack.get('serverPack'))

        return [{
            'version': modpack.get('version'),
            'size': None,
            'checksum': None,
            'url': url,
            'build': build
        }]
