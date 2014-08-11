import urllib2
import json


class loader_tekkit:

    base_url = 'http://www.technicpack.net'

    def __init__(self):
        pass

    def artifactURL(self, name):
        return self.base_url + '/api/modpack/' + name

    def getJSON(self, name):
        _url = self.artifactURL(name)
        response = urllib2.urlopen(_url)
        return json.loads(response.read())

    def load(self, channel, _):
        data = self.getJSON(channel['name'])
        builds = []

        builds.append({
            'version': data['version'],
            'size': None,
            'checksum': None,
            'url': data['url'],
            'build': 1
        })

        return builds
