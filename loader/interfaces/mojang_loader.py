import urllib2, json

class loader_mojang:

	url = 'http://s3.amazonaws.com/Minecraft.Download/versions/versions.json'
	download_url_base = 'https://s3.amazonaws.com/Minecraft.Download/versions/{0}/minecraft_server.{0}.jar'

	def getJSON(self):
		response = urllib2.urlopen(self.url)
		return json.loads(response.read())

	def create_build_numbers(self, builds):
		numbers = dict()
		builds.sort(key=lambda b: b['releaseTime'])
		counter = 1
		for build in builds:
			numbers[build['id']] = counter
			counter += 1
		return numbers

	def load(self, channel, last_build):
		data = self.getJSON()

		build_numbers = self.create_build_numbers(data['versions'])

		builds = []
		for build in data['versions']:
			if build['type'] != channel['name']: continue

			build_number = build_numbers[build['id']]
			if build_number <= last_build: continue

			builds.append({
				'version': build['id'],
				'size': None,
				'checksum': None,
				'url': self.download_url_base.format(build['id']),
				'build': build_number
			})

		return builds
