import requests, re

class loader_pixelmon:

	base_url = 'http://mirror5.pixelmongaming.com'

	def getData(self, name):

		r = requests.get(self.base_url)
		p = re.compile('download\\/[A-z]+ ([0-9\\.]+).zip')
		version = p.findall(r.content)[0]

		url = 'http://mirror2.pixelmongaming.com/download/Pixelmon%20'+version+'.zip'

		site = requests.head(url)
		
		size = site.headers['content-length'];

		return {'url' : url, 'version' : version, 'size' : size}

	def load(self, channel, last_build):
		data = self.getData(channel['name'])
		builds = []

		builds.append({
			'version': data['version'],
			'size': data['size'],
			'checksum': None,
			'url': data['url'],
			'build': 1
			})

		return builds