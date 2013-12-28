import urllib2, json, re, sys, math

class loader_jenkins:

	def makeProgressBar(self, message):
		toolbar_width = 20

		sys.stdout.write("\n" + message + "\n")

		sys.stdout.write("[%s]" % (" " * toolbar_width))
		sys.stdout.flush()
		sys.stdout.write("\b" * (toolbar_width+1))

	def incrementProgressBar(self):
		sys.stdout.write("-")
		sys.stdout.flush()

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
				m = re.search('[0-9].[0-9].[0-9]{1,2}(-R[0-9].[0-9])?', i)
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

		every = math.floor(len(data['builds']) / 20)
		if every > 0:
			self.makeProgressBar('Grabbing from Jenkins...')

		for i, build in enumerate(data['builds']):
			if every > 0 and i % every == 0:
				self.incrementProgressBar()

			if build['number'] <= last_build: continue

			out = self.getBuildData(build)
			if out: builds.append(out)

		return builds
