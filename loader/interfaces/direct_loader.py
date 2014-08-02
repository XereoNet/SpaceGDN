import urllib2, json

class loader_direct:

	def load(self, channel, last_build):
		builds = []

		builds.append({
			'version': channel['version'],
			'size': None,
			'checksum': None,
			'url': channel['url'],
			'build': 1
		})

		return builds