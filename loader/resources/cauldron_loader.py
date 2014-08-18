import requests
import re
import datetime
from ..resource_bases import Downloader
from bs4 import BeautifulSoup


class Cauldron(Downloader):

    base_url = 'http://files.minecraftforge.net/Cauldron/'

    def __init__(self):
        pass

    def load_pack(self, path, url):
        r = requests.get(url, stream=True)
        with open(path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    def parse_rows(self, row):
        version, minecraft, release, downloads = row.find_all('td')
        url = downloads.find_all('a').pop()['href']

        return {
            '$parents': [
                {
                    '$id': 'minecraft',
                    'resource': 'game',
                    'name': 'Minecraft'
                }, {
                    '$id': 'cauldron',
                    'resource': 'type',
                    'name': 'Cauldron',
                    'author': 'MinecraftForge',
                    'description': ''
                }, {
                    '$id': minecraft.text,
                    'resource': 'version',
                    'version': minecraft.text,
                    'mc_version': minecraft.text
                }
            ],
            '$id': version.text,
            '$load': lambda path: self.download(url, path),
            '$patched': False,
            'resource': 'build',
            'created': datetime.datetime.strptime(release.text, '%m/%d/%Y %I:%M:%S %p'),
            'build': re.sub(r'[^0-9]', '', version.text),
            'url': url,
        }

    def get_rows(self):
        r = requests.get(self.base_url)
        soup = BeautifulSoup(r.content)
        tables = [s.find('table') for s in soup.find_all(class_="builds")]

        out = []
        for table in tables:
            out.extend(table.find_all('tr')[1:10])

        return out

    def items(self):
        return map(self.parse_rows, self.get_rows())