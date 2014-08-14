import urllib.request, urllib.error, urllib.parse
import json
import datetime
import re


class loader_mojang:

    url = 'http://s3.amazonaws.com/Minecraft.Download/versions/versions.json'
    download_url_base = ('https://s3.amazonaws.com/Minecraft.Download/versions'
                         '/{0}/minecraft_server.{0}.jar')

    def __init__(self):
        pass

    def getJSON(self):
        response = urllib.request.urlopen(self.url)
        return json.loads(response.read())

    def totimestamp(self, dt, epoch=datetime.datetime(1970, 1, 1)):
        td = dt - epoch
        return ((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)
                / 1e6)

    def load(self, channel, last_build):
        data = self.getJSON()

        builds = []
        for build in data['versions']:
            if build['type'] != channel['name']:
                continue

            time = datetime.datetime.strptime(re.sub(r'\+[0-9]{2}:[0-9]{2}$',
                                                     '',
                                                     build['releaseTime']),
                                              '%Y-%m-%dT%H:%M:%S')
            build_number = int(self.totimestamp(time))

            if build_number <= last_build:
                continue

            builds.append({
                'version': build['id'],
                'size': None,
                'checksum': None,
                'url': self.download_url_base.format(build['id']),
                'build': build_number
            })

        return builds
