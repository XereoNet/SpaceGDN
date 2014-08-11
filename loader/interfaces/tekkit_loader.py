import urllib2, json

class loader_tekkit:

    base_url = 'http://www.technicpack.net'

    def artifactURL(self, name):
        return self.base_url + '/api/modpack/' + name

    def getJSON(self, name):
        _url = self.artifactURL(name)
        response = urllib2.urlopen(_url)
        return json.loads(response.read())

    def load(self, channel, last_build):
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