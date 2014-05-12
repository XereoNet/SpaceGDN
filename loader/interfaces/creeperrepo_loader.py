import requests, urllib
from lxml import etree as ET

class loader_creeperrepo:

	base_url = 'http://www.creeperrepo.net'

	def artifactURL(self, name):
		return self.base_url + '/FTB2/static/modpacks.xml'

	def getData(self, name, version, file_):

		url = self.base_url + '/FTB2/' + urllib.quote_plus('modpacks^'+name+'^'+version+'^'+file_)

		# site = requests.head(url)

		# size = site.headers['content-length'];

		return url

	def getXML(self, name):
		r = requests.get(self.artifactURL(self))
		return ET.fromstring(r.content)

	def load(self, channel, last_build):
		data = self.getXML(channel['name'])
		builds = []

		for modpack in data.findall('modpack'):

			if modpack.get('serverPack') == "": continue

			if modpack.get('repoVersion') != None:
				version = modpack.get('repoVersion')
			else:
				version = modpack.get('version')

			url = self.getData(modpack.get('dir'), version, modpack.get('serverPack'))

			builds.append({
				'version': version,
				'size': None,
				'checksum': None,
				'url': url,
				'build': 1
			})

		return builds