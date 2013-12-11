import urllib2, json, re

class loader_jenkins:

	def apiURL(self, url):
		if not url.endswith('/'): url += '/'
		return url + 'api/json?pretty=true'

	def artifactURL(self, url, artifacts):
		if not url.endswith('/'): url += '/'
		return url + 'artifact/' + artifacts[0]['relativePath']

	def getJSON(self, url):
		_url = self.apiURL(url)
		response = urllib2.urlopen(_url)
		return json.loads(response.read())

	def getBuildData(self, build):
		data = self.getJSON(build['url'])

		if data['result'] != 'SUCCESS': return False

		def getVersion (i):

			if isinstance(i, list):
				for item in i:
					out = getVersion(item)
					if out: return out

			if isinstance(i, dict):
				for key, item in i.iteritems():
					out = getVersion(item)
					if out: return out

			if isinstance(i, (basestring, str)):
				m = re.search('[0-9].[0-9].[0-9]{1,2}', i)
				if m: return m.group(0)

			return False

		return {
			'build': data['number'],
			'version': getVersion(data['artifacts']),
			'url': self.artifactURL(build['url'], data['artifacts'])
		}


	def load(self, channel, last_build):
		data = self.getJSON(channel['url'])
		builds = []

		for build in data['builds']:
			if build['number'] <= last_build: continue

			out = self.getBuildData(build)
			if out: builds.append(out)

		return builds