import urllib2, json

class loader_craftbukkit:

	base_url = 'http://dl.bukkit.org'

	def artifactURL(self, name):
		return self.base_url + '/api/1.0/downloads/projects/craftbukkit/artifacts/' + name

	def getJSON(self, name):
		_url = self.artifactURL(name)
		response = urllib2.urlopen(_url)
		return json.loads(response.read())

	def load(self, channel, last_build):
		data = self.getJSON(channel['name'])
		builds = []

		for build in data['results']:
			if build['build_number'] <= last_build or build['is_broken']: continue

			builds.append({
				'version': build['version'],
				'size': build['file']['size'] / 1024,
				'checksum': build['file']['checksum_md5'],
				'url': self.base_url + build['file']['url'],
				'build': build['build_number']
			})

		return builds